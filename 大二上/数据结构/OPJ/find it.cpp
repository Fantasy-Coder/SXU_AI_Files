#include<iostream>
#include<cstdio>
using namespace std;

int fx[100010];
int flag[100010];
void initial1(int n){
    for(int i=1;i<=n;i++){
        fx[i]=i;
        flag[i]=0;
    }
}

int find1(int a){
    int t=0;
    if(fx[a]==a){
        return a;
    }else{
        t = find1(fx[a]);
        flag[a] = (flag[fx[a]] +flag[a]) % 2;
        fx[a] = t;
        return fx[a];
    }
}

void union1(int a,int b){
    int p = find1(a);
    int q = find1(b);
    fx[p] = q;
    if(flag[b] == 0)
        flag[p] = 1-flag[a];
    else
        flag[p] = flag[a];

}

int main(){
    int t,n,m,x,y;
    char ch;
    scanf("%d",&t);
    while(t--){
         scanf("%d %d",&n,&m);
        initial1(n);
        while (m--)
        {
            getchar();
            scanf("%c %d %d",&ch,&x,&y);
            if(ch=='A'){
                if(find1(x)!=find1(y)){
                    cout<<"Not sure yet."<<endl;
                }
                else if(flag[x]==flag[y]){
                    cout<<"In the same gang."<<endl;
                }
                else {
                    cout<<"In different gangs."<<endl;
                }
            }
            else if(ch=='D'){
                union1(x,y);
            }
        
        }

    }
    system("pause");
    return 0;
    
}
