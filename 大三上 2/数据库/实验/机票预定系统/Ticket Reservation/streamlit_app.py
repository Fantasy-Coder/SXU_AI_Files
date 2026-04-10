"""
Streamlit 原型：登录/注册、航班搜索、购票支付、订单查看，管理员可浏览所有航班与订单。
运行：
    streamlit run streamlit_app.py
"""
import base64
from pathlib import Path
from typing import Any, Dict

import streamlit as st

from business_operations.service import TicketingService, PAY_UNPAID, ORDER_PENDING


st.set_page_config(page_title="机票预订系统", layout="wide")


def _inject_global_styles() -> None:
    """Global UI polish: remove Streamlit decoration bar and keep a simple, consistent palette."""
    st.markdown(
        """
        <style>
        :root {
            --accent: #2563eb;
            --accent-2: #0ea5e9;
            --ink: #0f172a;
        }
        /* Remove the red→yellow decoration bar at the very top */
        div[data-testid="stDecoration"] { display: none !important; }

        /* Keep header transparent */
        header[data-testid="stHeader"] { background: transparent; }

        /* Layout + layered gradient background to avoid flat white */
        div[data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 18% 20%, rgba(37, 99, 235, 0.12), transparent 32%),
                radial-gradient(circle at 82% 5%, rgba(14, 165, 233, 0.14), transparent 30%),
                linear-gradient(135deg, #e0f2fe 0%, #eef2ff 100%);
        }
        div.block-container {
            padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px;
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid rgba(37, 99, 235, 0.08);
            border-radius: 18px;
            box-shadow: 0 16px 44px rgba(15, 23, 42, 0.08);
        }

        /* Title tint: gradient ink instead of plain white */
        div.block-container h1 {
            background: linear-gradient(120deg, var(--accent), var(--accent-2));
            -webkit-background-clip: text;
            color: transparent !important;
            font-weight: 800;
            letter-spacing: 0.5px;
        }
        div.block-container h2 { color: var(--ink) !important; }

        /* Tabs: single accent color, minimal styling */
        div[data-testid="stTabs"] {
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 14px;
            padding: 0.35rem 0.6rem;
        }
        div[data-testid="stTabs"] button {
            font-weight: 600;
            margin-right: 8px;
            padding: 10px 14px;
            border-radius: 10px;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            border-bottom: 3px solid var(--accent);
            color: var(--accent);
        }

        /* Primary buttons微调，圆角一致 */
        button[kind="primary"], .stButton>button {
            border-radius: 10px;
            background: linear-gradient(120deg, var(--accent), var(--accent-2));
            color: #fff;
            border: none;
            box-shadow: 0 10px 24px rgba(37,99,235,0.18);
            padding: 8px 14px;
            min-height: 36px;
        }
        .stButton>button:hover { filter: brightness(1.05); }

        /* 结果表格行间距 & 边框 */
        div[data-testid="stHorizontalBlock"] > div > div:has(> div[data-testid="column"]) {
            padding: 10px 12px;
            border-bottom: 1px solid rgba(15,23,42,0.06);
        }
        div[data-testid="stHorizontalBlock"] > div:first-child > div:has(> div[data-testid="column"]) {
            border-top: 1px solid rgba(15,23,42,0.06);
        }

        /* Forms: add breathing room + light border (avoid heavy backgrounds so login cover still shows) */
        div[data-testid="stForm"] {
            border: 1px solid rgba(15, 23, 42, 0.10);
            border-radius: 14px;
            padding: 16px 16px 8px 16px;
            background: rgba(255, 255, 255, 0.78);
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
        }
        /* Alerts with a little accent edge */
        div[data-testid="stAlert"] {
            border-left: 4px solid var(--accent);
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner=False)
def get_service():
    return TicketingService()


def _image_as_base64(path: str) -> str:
    img_path = Path(path)
    if not img_path.is_absolute():
        img_path = Path(__file__).resolve().parent / img_path
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def login_panel(svc: TicketingService):
    st.subheader("登录")
    # 尝试使用项目内的相对路径加载封面图片；若不存在则降级为纯色/渐变背景，避免抛出异常或留下 traceback
    cover_path = Path(__file__).resolve().parent / "JPG" / "登录封面.jpeg"
    if cover_path.exists():
        try:
            b64 = _image_as_base64(cover_path)
            bg_css = f"background: linear-gradient(180deg, rgba(8, 10, 26, 0.65), rgba(8, 10, 26, 0.78)), url(data:image/jpeg;base64,{b64}) !important;"
            title_color = "#ffffff"
        except Exception:
            bg_css = "background: linear-gradient(180deg,#f8fafc,#eef2ff) !important;"
            title_color = "var(--ink)"
    else:
        bg_css = "background: linear-gradient(180deg,#f8fafc,#eef2ff) !important;"
        title_color = "var(--ink)"

    st.markdown(
        f"""
        <style>
        /* 登录区背景图覆盖表单与注册按钮区域 */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stForm"]) {{
            position: relative;
            padding: 32px 32px 24px 32px;
            border-radius: 18px;
            {bg_css}
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: scroll !important;
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.25);
            overflow: hidden;
        }}
        /* 登录区内的标题也强制为白色或适配色，避免被背景或半透明遮罩变灰 */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stForm"]) h1,
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stForm"]) h2,
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stForm"]) h3 {{
            color: {title_color} !important;
        }}
        /* 提升表单可读性 */
        div[data-testid="stForm"] label {{ color: #f7f9fc; font-weight: 600; }}
        div[data-testid="stForm"] input {{ background: rgba(255, 255, 255, 0.92); color: #0c0c0c; }}
        div[data-testid="stForm"] .stButton>button {{ width: 100%; font-weight: 700; }}
        /* 注册按钮样式，与背景融合 */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stForm"]) .stButton>button {{
            background: rgba(255, 255, 255, 0.9);
            color: #101225;
            border: 1px solid rgba(255, 255, 255, 0.5);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.form("login_form"):
        username = st.text_input("用户名", value="admin")
        password = st.text_input("密码", type="password", value="admin123")
        submitted = st.form_submit_button("登录")
    if submitted:
        try:
            user = svc.authenticate(username, password)
            if user:
                st.session_state["user"] = user
                st.session_state["page"] = "main"
                st.success("登录成功")
                st.rerun()
            else:
                st.error("用户名或密码错误")
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            st.error("登录失败，请稍后再试")
    if st.button("注册新用户"):
        st.session_state["page"] = "register"
        st.rerun()


def register_panel(svc: TicketingService):
    st.subheader("注册")
    with st.form("register_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        name = st.text_input("姓名")
        phone = st.text_input("电话")
        email = st.text_input("邮箱")
        submitted = st.form_submit_button("注册")
    if submitted:
        try:
            uid = svc.register_user(username, password, name, phone, email)
            st.success(f"注册成功，用户ID={uid}")
            st.session_state["page"] = "login"
            st.rerun()
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))
    if st.button("返回登录", key="register_return_login"):
        st.session_state["page"] = "login"
        st.rerun()


def search_flights_ui(svc: TicketingService, is_admin: bool = False):
    import pandas as pd  # noqa: F401  # reserved for future table formatting
    with st.form("search_form"):
        col1, col2, col3, col4 = st.columns(4)
        departure = col1.text_input("出发地")
        destination = col2.text_input("目的地")
        date_prefix = col3.text_input("出发日期前缀", value="2025-01")
        airline = col4.text_input("航空公司包含")
        col5, col6 = st.columns(2)
        price_min = col5.number_input("最低票价", min_value=0.0, value=0.0)
        price_max = col6.number_input("最高票价", min_value=0.0, value=2000.0)
        submitted = st.form_submit_button("查询")
    if submitted:
        flights = svc.search_flights(
            departure=departure or None,
            destination=destination or None,
            date_prefix=date_prefix or None,
            airline=airline or None,
            price_min=price_min or None,
            price_max=price_max or None,
        )
        st.session_state["last_flights"] = flights
    flights = st.session_state.get("last_flights", [])
    if flights:
        st.markdown("#### 查询结果")
        columns = ["航班ID", "航班号", "航空公司", "出发地", "目的地", "出发时间", "到达时间", "票价", "余座", "状态", "操作"]
        # 更美观的列宽，操作按钮靠状态旁
        col_widths = [1,1.2,1.8,1.2,1.2,2,2,1.2,1,1.0,1.0]
        header_cols = st.columns(col_widths)
        for j, col_name in enumerate(columns):
            header_cols[j].markdown(f"<div style='text-align:center;font-weight:bold'>{col_name}</div>", unsafe_allow_html=True)
        # 数据行
        for row in flights:
            cols = st.columns(col_widths)
            for j, v in enumerate(row):
                # 票价加￥，内容居中
                if j == 7:
                    cols[j].markdown(f"<div style='text-align:center'>￥{v:.2f}</div>", unsafe_allow_html=True)
                # 状态加颜色
                elif j == 9:
                    color = "green" if v == "正常" else ("red" if v == "停飞" else "orange")
                    cols[j].markdown(f"<div style='text-align:center;color:{color}'>{v}</div>", unsafe_allow_html=True)
                else:
                    cols[j].markdown(f"<div style='text-align:center'>{v}</div>", unsafe_allow_html=True)
            # 操作按钮（列索引10紧邻状态）
            op_col = cols[10]
            if is_admin:
                if op_col.button("编辑", key=f"goto_edit_{row[0]}"):
                    st.session_state["admin_tab_target"] = "编辑/删除航班"
                    st.session_state["admin_focus_flight"] = row[0]
                    st.session_state["page"] = "main"
                    st.rerun()
            elif row[8] > 0 and row[9] == "正常":
                if op_col.button(" 购票", key=f"buy_{row[0]}"):
                    st.session_state["buy_flight_id"] = row[0]
                    st.session_state["page"] = "purchase"
                    st.rerun()
            else:
                op_col.markdown("<div style='text-align:center;color:gray'>不可购票</div>", unsafe_allow_html=True)
    else:
        if is_admin:
            st.info("未找到航班，去增加一个吧。")
            if st.button("去增加航班", key="no_result_add"):
                st.session_state["admin_tab_target"] = "增加航班"
                st.session_state["page"] = "main"
                st.rerun()
        else:
            st.info("暂无符合条件的航班")


def purchase_ui(svc: TicketingService, user_id: int):
    st.markdown("### 购票 / 支付")
    flights = st.session_state.get("last_flights", [])
    flight_options = {f"{f[1]} {f[3]}->{f[4]} {f[5]} 余{f[8]}": f[0] for f in flights}
    flight_label = st.selectbox("选择航班", list(flight_options.keys()) if flight_options else [])
    flight_id = flight_options.get(flight_label)

    st.markdown("#### 乘客信息")
    cname = st.text_input("姓名", key="p_name")
    cid = st.text_input("身份证号", key="p_idcard")
    cphone = st.text_input("电话", key="p_phone")
    cemail = st.text_input("邮箱", key="p_email")
    class_type = st.selectbox("舱位", ["经济舱", "商务舱", "头等舱"], index=0)

    if st.button("创建订单并出票"):
        try:
            pid = svc.add_passenger(cname, cid, cphone, cemail)
            order_id, order_no = svc.create_order(user_id, [pid], flight_id, class_type=class_type)
            st.session_state["last_order_id"] = order_id
            st.success(f"下单成功：{order_no} (ID={order_id})")
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))

    order_id = st.session_state.get("last_order_id")
    if order_id:
        if st.button("支付订单"):
            try:
                svc.pay_order(order_id)
                st.success("支付成功")
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))
        try:
            info = svc.describe_order(order_id)
            st.write("订单:", info["order"])
            st.write("机票:")
            st.table(info["tickets"])
        except Exception as exc:  # noqa: BLE001
            st.warning(str(exc))


def user_orders_ui(svc: TicketingService, user_id: int):
    st.markdown("### 我的订单")
    orders = svc.list_orders(user_id)
    if not orders:
        st.info("暂无订单")
        return

    # 卡片样式 CSS（每个订单作为独立卡片显示）
    st.markdown(
        """
        <style>
        .order-card{border:1px solid rgba(15,23,42,0.06);border-radius:12px;padding:14px;margin-bottom:16px;background:#ffffff}
        .order-header{display:flex;align-items:center;justify-content:space-between}
        .order-meta{color:#6b7280;margin-top:6px;margin-bottom:8px}
        .order-actions button{margin-left:8px}
        </style>
        """,
        unsafe_allow_html=True,
    )

    for order in orders:
        order_id, order_no, contact_id, order_date, total_amount, payment_status, order_status = order
        with st.container():
            st.markdown(f"<div class='order-card'>", unsafe_allow_html=True)
            cols = st.columns([7.5, 2.5])
            header_html = f"<div style='font-weight:700;font-size:16px'>订单号：{order_no} &nbsp; 总金额：￥{total_amount:.2f} &nbsp; 状态：{order_status} &nbsp; 支付：{payment_status}</div>"
            cols[0].markdown(header_html, unsafe_allow_html=True)
            action_cols = cols[1].columns(2)
            # 操作按钮：查看订单（可切换） / 退票或删除
            if action_cols[0].button("查看订单", key=f"view_{order_id}"):
                if st.session_state.get("view_order_id") == order_id:
                    st.session_state.pop("view_order_id", None)
                else:
                    st.session_state["view_order_id"] = order_id

            if order_status not in ("已取消",):
                if action_cols[1].button("退票/删除", key=f"cancel_{order_id}"):
                    try:
                        svc.cancel_order(order_id)
                        st.success("退票成功，订单已取消")
                        if st.session_state.get("view_order_id") == order_id:
                            st.session_state.pop("view_order_id", None)
                        st.rerun()
                    except Exception as exc:
                        st.error(f"退票失败: {exc}")
            else:
                if action_cols[1].button("删除订单", key=f"delete_{order_id}"):
                    try:
                        svc.db.execute("DELETE FROM Orders WHERE OrderID=?", (order_id,))
                        st.success("订单已永久删除")
                        if st.session_state.get("view_order_id") == order_id:
                            st.session_state.pop("view_order_id", None)
                        st.rerun()
                    except Exception as exc:
                        st.error(f"删除失败: {exc}")

            cols[0].markdown(f"<div class='order-meta'>下单时间：{order_date}</div>", unsafe_allow_html=True)

            # 如果当前卡片被选中查看，展示订单详情与机票表格
            if st.session_state.get("view_order_id") == order_id:
                try:
                    tickets = svc.list_tickets(order_id)
                    if tickets:
                        import pandas as pd

                        def fix_row(row):
                            row = list(row)
                            if len(row) < 9:
                                row += [""] * (9 - len(row))
                            elif len(row) > 9:
                                row = row[:9]
                            return tuple(row)

                        fixed_tickets = [fix_row(row) for row in tickets]
                        df = pd.DataFrame(
                            fixed_tickets,
                            columns=["机票ID", "航班号", "座位号", "票价", "舱位", "状态", "乘客姓名", "出发时间", "到达时间"],
                        )
                        st.markdown("<div style='margin-top:8px'>", unsafe_allow_html=True)
                        st.dataframe(
                            df,
                            use_container_width=True,
                            column_config={
                                "座位号": st.column_config.TextColumn(width=70),
                                "票价": st.column_config.NumberColumn(format="￥%.2f", width=70),
                            },
                        )
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        cols[0].write("无机票信息")
                except Exception as exc:
                    st.warning(str(exc))

            st.markdown("</div>", unsafe_allow_html=True)


def admin_flight_overview():
    """航班总览：只读表格。"""
    from flight_operations.flight_crud import FlightCRUD
    flight_crud = FlightCRUD()
    flights = flight_crud.get_flights()
    columns = ["航班ID", "航班号", "航空公司", "出发地", "目的地", "出发时间", "到达时间", "机型", "座位数", "余座", "票价", "状态"]
    import pandas as pd

    st.markdown("### 航班总览")
    df = pd.DataFrame(flights, columns=columns)
    st.dataframe(df, use_container_width=True)


def admin_add_flight():
    """增加航班：单独表单。"""
    from flight_operations.flight_crud import FlightCRUD
    flight_crud = FlightCRUD()

    st.markdown("### 增加航班")
    with st.form("add_flight_form"):
        fno = st.text_input("航班号")
        airline = st.text_input("航空公司")
        dep = st.text_input("出发地")
        dest = st.text_input("目的地")
        dtime = st.text_input("出发时间", value="2025-01-01 08:00")
        atime = st.text_input("到达时间", value="2025-01-01 10:00")
        aircraft = st.text_input("机型")
        seat_count = st.number_input("座位数", min_value=1, value=180)
        remain = st.number_input("余座", min_value=0, value=180)
        price = st.number_input("票价", min_value=0.0, value=500.0)
        status = st.selectbox("状态", ["正常", "停飞"])
        submitted = st.form_submit_button("添加航班")
    if submitted:
        ok = flight_crud.add_flight((fno, airline, dep, dest, dtime, atime, aircraft, seat_count, remain, price, status))
        if ok:
            new_id = getattr(flight_crud.db, "get_last_insert_id", lambda: None)()
            # 记录新航班ID并切换到编辑/删除标签页自动展开
            if new_id:
                st.session_state["admin_focus_flight"] = new_id
            st.session_state["admin_tab_target"] = "编辑/删除航班"
            st.success(f"添加成功，航班ID={new_id}" if new_id else "添加成功")
            st.rerun()
        else:
            st.error("添加失败")


def admin_edit_delete_flights():
    """编辑/删除航班：逐条展开，并可通过搜索跳转自动展开。"""
    from flight_operations.flight_crud import FlightCRUD
    flight_crud = FlightCRUD()
    flights = flight_crud.get_flights()
    target_flight = st.session_state.get("admin_focus_flight")

    st.markdown("### 编辑 / 删除航班")
    if not flights:
        st.info("暂无航班数据")
        return

    for row in flights:
        with st.expander(f"航班ID {row[0]} - {row[1]} {row[3]}->{row[4]}", expanded=target_flight == row[0]):
            with st.form(f"edit_flight_{row[0]}"):
                efno = st.text_input("航班号", value=row[1], key=f"efno_{row[0]}")
                eairline = st.text_input("航空公司", value=row[2], key=f"eairline_{row[0]}")
                edep = st.text_input("出发地", value=row[3], key=f"edep_{row[0]}")
                edest = st.text_input("目的地", value=row[4], key=f"edest_{row[0]}")
                edtime = st.text_input("出发时间", value=row[5], key=f"edtime_{row[0]}")
                eatime = st.text_input("到达时间", value=row[6], key=f"eatime_{row[0]}")
                eaircraft = st.text_input("机型", value=row[7], key=f"eaircraft_{row[0]}")
                eseat_count = st.number_input("座位数", min_value=1, value=row[8], key=f"eseat_{row[0]}")
                eremain = st.number_input("余座", min_value=0, value=row[9], key=f"eremain_{row[0]}")
                eprice = st.number_input("票价", min_value=0.0, value=row[10], key=f"eprice_{row[0]}")
                estatus = st.selectbox("状态", ["正常", "停飞"], index=0 if row[11] == "正常" else 1, key=f"estatus_{row[0]}")
                update = st.form_submit_button("保存修改")
                delete = st.form_submit_button("删除航班")
            if update:
                ok = flight_crud.update_flight(row[0], (efno, eairline, edep, edest, edtime, eatime, eaircraft, eseat_count, eremain, eprice, estatus))
                if ok:
                    st.success("修改成功")
                    st.rerun()
                else:
                    st.error("修改失败")
            if delete:
                ok = flight_crud.delete_flight(row[0])
                if ok:
                    st.success("删除成功")
                    st.rerun()
                else:
                    st.error("删除失败")
    if target_flight:
        st.session_state.pop("admin_focus_flight", None)


def admin_order_overview(svc: TicketingService):
    st.markdown("### 订单总览")
    orders = svc.list_orders(None)
    columns = ["订单ID", "订单号", "联系人ID", "下单时间", "总金额", "支付状态", "订单状态"]
    try:
        import pandas as pd

        df = pd.DataFrame(orders, columns=columns)
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.dataframe(orders, use_container_width=True)


def profile_ui(svc: TicketingService, user: Dict[str, Any]):
    st.markdown("### 个人信息")
    current = svc.get_user(user["UserID"])
    if not current:
        st.error("用户不存在")
        return
    idcard_row = svc.db.fetch_one("SELECT idcard FROM realname_auth WHERE name=?", (current["Name"],))
    idcard_val = idcard_row[0] if idcard_row else ""

    name = st.text_input("姓名", value=current.get("Name", ""))
    idcard = st.text_input("身份证号", value=idcard_val)
    phone = st.text_input("手机号", value=current.get("Phone") or "")
    email = st.text_input("邮箱", value=current.get("Email") or "")

    if st.button("保存信息"):
        try:
            svc.update_user_profile(user["UserID"], name, phone, email, idcard or None)
            st.session_state["user"] = svc.get_user(user["UserID"]) or user
            st.success("信息已更新")
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))


def account_ui(svc: TicketingService, user: Dict[str, Any]):
    st.markdown("### 账号信息")
    st.text_input("用户名", value=user.get("Username", ""), disabled=True)

    st.markdown("#### 修改密码")
    col1, col2 = st.columns(2)
    old_pwd = col1.text_input("当前密码", type="password")
    new_pwd = col1.text_input("新密码", type="password", key="new_pwd")
    confirm_pwd = col2.text_input("确认新密码", type="password", key="confirm_pwd")

    if st.button("保存密码"):
        try:
            if not old_pwd or not new_pwd or not confirm_pwd:
                raise ValueError("请输入完整的密码信息")
            if new_pwd != confirm_pwd:
                raise ValueError("两次输入的新密码不一致")
            svc.change_password(user["UserID"], old_pwd, new_pwd)
            st.success("密码修改成功，请重新登录")
            st.session_state.clear()
            st.session_state["page"] = "login"
            st.rerun()
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))


def main():
    svc = get_service()
    _inject_global_styles()

    # 顶部标题与退出按钮并排放置
    header_cols = st.columns([6, 1])
    with header_cols[0]:
        st.title("机票预订系统")
    with header_cols[1]:
        if "user" in st.session_state:
            if st.button("退出登录", key="logout_top"):
                st.session_state.clear()
                st.session_state["page"] = "login"
                st.rerun()

    # 页面流转控制
    page = st.session_state.get("page", "login")
    if page == "login":
        login_panel(svc)
        return
    if page == "register":
        register_panel(svc)
        return

    if "user" not in st.session_state:
        st.session_state["page"] = "login"
        st.rerun()
        return

    user = st.session_state["user"]
    is_admin = user.get("Username") == "admin"
    # 去掉顶部用户提示，仅保留右上角退出

    # 管理员强制回到主页，防止进入购票流程
    current_page = st.session_state.get("page", "main")
    if is_admin and current_page in ("purchase", "checkin"):
        current_page = "main"
        st.session_state["page"] = "main"

    # 页面流转
    if current_page == "main":
        if is_admin:
            admin_tabs = ["航班搜索", "航班总览", "编辑/删除航班", "增加航班", "订单总览"]
            default_tab = st.session_state.pop("admin_tab_target", st.session_state.get("admin_active_tab", admin_tabs[0]))
            active_tab = st.radio("管理导航", admin_tabs, horizontal=True, index=admin_tabs.index(default_tab) if default_tab in admin_tabs else 0, key="admin_active_tab")

            if active_tab == "航班搜索":
                search_flights_ui(svc, is_admin=True)
            elif active_tab == "航班总览":
                admin_flight_overview()
            elif active_tab == "编辑/删除航班":
                admin_edit_delete_flights()
            elif active_tab == "增加航班":
                admin_add_flight()
            elif active_tab == "订单总览":
                admin_order_overview(svc)
        else:
            tabs = ["航班搜索", "我的订单", "个人信息", "账号信息"]
            selected_tab = st.tabs(tabs)
            with selected_tab[0]:
                search_flights_ui(svc, is_admin=False)
            with selected_tab[1]:
                user_orders_ui(svc, user_id=user["UserID"])
            with selected_tab[2]:
                profile_ui(svc, user)
            with selected_tab[3]:
                account_ui(svc, user)
    elif current_page == "purchase":
        purchase_flow_ui(svc, user["UserID"])
    elif current_page == "checkin":
        checkin_seat_ui(svc, user_id=user["UserID"])
def purchase_flow_ui(svc: TicketingService, user_id: int):
    flight_id = st.session_state.get("buy_flight_id")
    if not flight_id:
        st.warning("未选择航班")
        if st.button("返回航班搜索"):
            st.session_state["page"] = "main"
            st.rerun()
        return
    # 展示航班信息
    flight = svc.db.fetch_one("SELECT FlightNo, Airline, Departure, Destination, DepartureTime, ArrivalTime, Price, RemainingSeats FROM Flight WHERE FlightID=?", (flight_id,))
    if not flight:
        st.error("航班不存在")
        return
    st.markdown(f"### 购票 - 航班信息")
    st.info(f"航班号：{flight[0]}  航空公司：{flight[1]}  {flight[2]}→{flight[3]}  出发：{flight[4]}  到达：{flight[5]}  票价：￥{flight[6]:.2f}  余座：{flight[7]}")
    # 支持多乘客 + 座位图选座（按乘客顺序一人一座）
    class_type = st.selectbox("舱位", ["经济舱", "商务舱", "头等舱"], index=0, key="class_type_buy")

    st.markdown("#### 乘客列表")
    passengers = st.session_state.get("purchase_passengers", [])

    def add_passenger_row():
        passengers.append({"name": "", "idcard": "", "phone": "", "email": "", "seat": None})
        st.session_state["purchase_passengers"] = passengers

    if not passengers:
        add_passenger_row()

    for idx, p in enumerate(passengers):
        st.markdown(f"**乘客 {idx+1}**")
        cols = st.columns(4)
        p["name"] = cols[0].text_input("姓名", value=p.get("name", ""), key=f"p_name_{idx}")
        p["idcard"] = cols[1].text_input("身份证号", value=p.get("idcard", ""), key=f"p_id_{idx}")
        p["phone"] = cols[2].text_input("电话", value=p.get("phone", ""), key=f"p_phone_{idx}")
        p["email"] = cols[3].text_input("邮箱", value=p.get("email", ""), key=f"p_email_{idx}")
        # 展示当前座位
        seat_label = p.get("seat") or "未选座"
        cols[0].markdown(f"当前座位：**{seat_label}**")
        # 删除乘客
        if cols[3].button("删除", key=f"del_{idx}"):
            passengers.pop(idx)
            st.session_state["purchase_passengers"] = passengers
            st.rerun()

    col_add, col_clear = st.columns([1,1])
    if col_add.button("添加乘客", key="add_passenger"):
        add_passenger_row()
        st.rerun()
    if col_clear.button("清空乘客", key="clear_passenger"):
        st.session_state.pop("purchase_passengers", None)
        st.rerun()

    # 座位图（按乘客顺序分配，点击已选座可取消该乘客座位）
    st.markdown("#### 选择座位")
    seat_count = svc._seat_count(flight_id)
    seats_per_row = 6
    seat_labels = ["A", "B", "C", "D", "E", "F"]
    used_raw = set(svc._existing_seats(flight_id))
    used_existing = set()
    # 兼容旧格式(E1...)与新格式(1A)
    for idx in range(1, seat_count + 1):
        row = (idx - 1) // seats_per_row + 1
        col = (idx - 1) % seats_per_row
        label = f"{row}{seat_labels[col]}"
        legacy = f"E{idx}"
        if label in used_raw or legacy in used_raw:
            used_existing.add(label)
    selected_seats = {p.get("seat") for p in passengers if p.get("seat")}

    total_rows = (seat_count + seats_per_row - 1) // seats_per_row
    seat_idx = 1

    def assign_seat_click(seat_label: str):
        # 如果该座位已分配给某乘客，则取消该乘客的座位
        for p in passengers:
            if p.get("seat") == seat_label:
                p["seat"] = None
                st.session_state["purchase_passengers"] = passengers
                st.rerun()
                return
        # 否则分配给第一个未选座的乘客
        for p in passengers:
            if not p.get("seat"):
                p["seat"] = seat_label
                st.session_state["purchase_passengers"] = passengers
                st.rerun()
                return
        st.warning("乘客已选满座位，先取消再重选")

    for r in range(total_rows):
        cols = st.columns([1,1,1,0.3,1,1,1])
        for c in range(seats_per_row):
            if seat_idx > seat_count:
                cols[c if c < 3 else c+1].markdown("&nbsp;")
                continue
            label = f"{r+1}{seat_labels[c]}"
            col_slot = cols[c if c < 3 else c+1]
            if label in used_existing:
                col_slot.button(f"❌\n{label}", key=f"seat_{label}", disabled=True)
            elif label in selected_seats:
                if col_slot.button(f"🟦\n{label}", key=f"seat_{label}"):
                    assign_seat_click(label)
            else:
                if col_slot.button(f"🟩\n{label}", key=f"seat_{label}"):
                    assign_seat_click(label)
            seat_idx += 1

    # 下单
    if st.button("创建订单并支付"):
        try:
            if not passengers:
                raise ValueError("请先添加乘客")
            # 需全部乘客都已选座
            if any(not p.get("seat") for p in passengers):
                raise ValueError("请为每位乘客选座")
            # 校验实名
            for p in passengers:
                real = svc.db.fetch_one("SELECT 1 FROM realname_auth WHERE name=? AND idcard=?", (p.get("name"), p.get("idcard")))
                if not real:
                    raise ValueError(f"实名认证失败: {p.get('name')}")
            payload = [
                {
                    "name": p.get("name"),
                    "idcard": p.get("idcard"),
                    "phone": p.get("phone"),
                    "email": p.get("email"),
                }
                for p in passengers
            ]
            seats = [p.get("seat") for p in passengers]
            order_id, order_no = svc.create_order(user_id, payload, flight_id, class_type=class_type, seat_labels=seats)
            svc.pay_order(order_id)
            st.session_state.pop("purchase_passengers", None)
            st.session_state["last_order_id"] = order_id
            st.session_state["page"] = "main"
            st.success(f"下单并支付成功，订单号：{order_no}，可在‘我的订单’查看")
            st.rerun()
        except Exception as exc:
            st.error(str(exc))
    if st.button("返回航班搜索", key="back_to_search"):
        st.session_state["page"] = "main"
        st.rerun()
def checkin_seat_ui(svc: TicketingService, user_id: int):
    st.markdown("### 值机选座")
    # 查询用户所有未选座的机票
    tickets = svc.list_user_tickets(user_id)
    if not tickets:
        st.info("暂无可选座的机票")
        return
    ticket_options = {f"订单{t['OrderNo']} 航班{t['FlightNo']} {t['Departure']}->{t['Destination']} {t['Date']} 乘客:{t['PassengerName']}": t['TicketID'] for t in tickets}
    ticket_label = st.selectbox("选择机票", list(ticket_options.keys()) if ticket_options else [])
    ticket_id = ticket_options.get(ticket_label)
    if not ticket_id:
        return
    # 查询该航班所有座位和已占用座位
    row = svc.db.fetch_one("SELECT FlightID FROM Ticket WHERE TicketID=?", (ticket_id,))
    if not row:
        st.warning("机票异常")
        return
    flight_id = row[0]
    seat_count = svc._seat_count(flight_id)
    used = set(svc._existing_seats(flight_id))
    # 假设每排6座，生成座位布局
    seats_per_row = 6
    total_rows = (seat_count + seats_per_row - 1) // seats_per_row
    seat_labels = [f"{chr(65 + i)}" for i in range(seats_per_row)]  # A-F
    seat_grid = []
    for r in range(total_rows):
        row_seats = []
        for c in range(seats_per_row):
            idx = r * seats_per_row + c + 1
            if idx > seat_count:
                row_seats.append(None)
            else:
                row_seats.append(f"E{idx}")
        seat_grid.append(row_seats)

    st.markdown("#### 请选择座位：")
    selected_seat = st.session_state.get("selected_seat")
    # Streamlit原生按钮+emoji座位图
    selected_seat = st.session_state.get("selected_seat")
    st.markdown("#### 请选择座位：")
    # 3-3布局，ABC  DEF，中间留过道
    seats_per_row = 6
    seat_labels = ["A", "B", "C", "D", "E", "F"]
    total_rows = (seat_count + seats_per_row - 1) // seats_per_row
    seat_idx = 1
    for r in range(total_rows):
        cols = st.columns([1,1,1,0.3,1,1,1])  # 3+3布局，中间为过道
        for c in range(seats_per_row):
            if seat_idx > seat_count:
                cols[c if c < 3 else c+1].markdown("&nbsp;")
                continue
            label = f"{r+1}{seat_labels[c]}"  # 1A, 1B, ...
            # 统一用label作为座位号
            seat = label
            if seat in used:
                cols[c if c < 3 else c+1].button(f"❌\n{label}", key=f"seat_{seat}", disabled=True)
            elif selected_seat == seat:
                if cols[c if c < 3 else c+1].button(f"🟦\n{label}", key=f"seat_{seat}"):
                    st.session_state["selected_seat"] = seat
            else:
                if cols[c if c < 3 else c+1].button(f"🟩\n{label}", key=f"seat_{seat}"):
                    st.session_state["selected_seat"] = seat
                    selected_seat = seat
            seat_idx += 1
    if selected_seat:
        st.success(f"已选择座位：{selected_seat}")
        if st.button("确认选座", key="confirm_seat"):
            try:
                import time
                svc.checkin_seat(ticket_id, selected_seat)
                st.success(f"值机成功，购票完成！座位号：{selected_seat}")
                st.session_state.pop("selected_seat", None)
                st.info("3秒后自动跳转到‘我的订单’...")
                time.sleep(3)
                st.session_state["page"] = "main"
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


if __name__ == "__main__":
    main()
