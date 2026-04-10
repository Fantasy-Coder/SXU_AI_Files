"""
业务流程演示：使用 TicketingService 完成查询、购票、支付、退票/改签
运行：python business_operations/demo_workflow.py
"""
import os
import sys
from pprint import pprint

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from business_operations.service import TicketingService


def main():
    svc = TicketingService()
    try:
        # 准备用户和乘客
        try:
            user_id = svc.register_user("demo_user", "123456", "演示用户", "13900000000", "demo@example.com")
        except ValueError:
            user_id = svc.db.fetch_one("SELECT UserID FROM User WHERE Username=?", ("demo_user",))[0]
        passenger_id = svc.add_passenger("演示旅客", "110101199001018888", "13900000001", "demo_p@example.com")

        print("\n1) 搜索航班 北京->上海 (2025-01-01)")
        flights = svc.search_flights(departure="北京", destination="上海", date_prefix="2025-01-01")
        for f in flights:
            print(f)
        if not flights:
            print("无航班可用，提前退出")
            return

        flight_id = flights[0][0]
        print(f"\n2) 选择 FlightID={flight_id} 下单")
        order_id, order_no = svc.create_order(user_id, [passenger_id], flight_id)
        print("生成订单:", order_id, order_no)

        print("\n3) 支付订单")
        svc.pay_order(order_id)

        print("\n4) 订单详情")
        pprint(svc.describe_order(order_id))

        print("\n5) 退票演示（删除该票并回补余座）")
        tickets = svc.list_tickets(order_id)
        if tickets:
            svc.refund_ticket(tickets[0][0])
            pprint(svc.describe_order(order_id))
        else:
            print("订单下无票据")

    finally:
        svc.close()


if __name__ == "__main__":
    main()
