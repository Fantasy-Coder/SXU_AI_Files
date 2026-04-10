#include<bits/stdc++.h>
using namespace std;

int father[100005];
int n,m,a,b;
int tmp=0;

int find(int x)
{
    if(father[x]==-1)return x;
    else return find(father[x]);
}

int main()
{
    
    while(true)
    {
        cin>>n>>m;
        memset(father,-1,sizeof(father));
        if(n==0&&m==0)break;
        for(int i=1;i<=m;i++)
        {
            cin>>a>>b;
            int fa=find(a),fb=find(b);
            if(fa!=fb)father[fa]=fb,n--;
        }
        cout<<"Case "<<++tmp<<": "<<n<<endl;
    }
    return 0;
}
