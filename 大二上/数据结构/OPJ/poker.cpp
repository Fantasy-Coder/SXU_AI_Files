#include<iostream>
#include<queue>
using namespace std;
int main(){
    int n;
    scanf("%d",&n);
    string card[n];
    queue<string> q[9];
    for(int i=0;i<n;i++){
        cin>>card[i];
        q[card[i][1]-'0'-1].push(card[i]);
    }
    int k=0;
    for(int i=0;i<9;i++){
        printf("Queue%d:",i+1);
        while(!q[i].empty()){
            card[k++]=q[i].front();
            printf("%s ",q[i].front().c_str());
            q[i].pop();
        }
        printf("\n");
    }
    for(int i=0;i<n;i++){
        q[card[i][0]-'A'].push(card[i]);
    }
    k=0;
    for(int i=0;i<4;i++){
        printf("Queue%c:",'A'+i);
        while(!q[i].empty()){
            card[k++]=q[i].front();
            printf("%s ",q[i].front().c_str());
            q[i].pop();
        }
        printf("\n");
    }
    for(int i=0;i<n;i++){
        printf("%s ",card[i].c_str());
    }
    printf("\n");
}