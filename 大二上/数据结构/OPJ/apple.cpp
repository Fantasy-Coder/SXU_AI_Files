#include <iostream>
using namespace std;
int fun(int m,int n) {
    if(n==1||m==1) return 1;
    if(m<n) return fun(m,m);
    else if(m==n) return fun(m,n-1)+1;
    else return fun(m-n,n)+fun(m,n-1);//m>n时，若有一个盘子不放，则将m个放入n-1，若每个盘子都有,则结果与m-n个相同
}

int main() {
    int t,m,n;
    cin>>t;
    while(t-->0){
        cin>>m>>n;
        cout<<fun(m,n)<<endl;
    }
    return 0;
}