#include<iostream>
#include<algorithm>
using namespace std;
struct SortOrder{
    string str;
    int Count{};
    int Order{};
    inline bool operator<(const SortOrder& b) const{
        if(Count!=b.Count) return Count<b.Count;
        else return Order<b.Order;
    }
};
char temp[55];
inline void Merge(string& str,int first,int mid,int last,int& count){
    int i=first;int j=mid+1;int cur=first;
    while(i<=mid&&j<=last){
        if(str[i]<=str[j]){
            temp[cur++]=str[i++];
        }
        else{
            temp[cur++]=str[j++];
            count+=mid-i+1;
        }
    }
    while(i<=mid){
        temp[cur++]=str[i++];
    }
    while(j<=last){
        temp[cur++]=str[j++];
    }
    for(int k=first;k<=last;k++){
        str[k]=temp[k];
    }
}
inline void MergeSort(string& str,int first,int last,int& count){
    if(first==last) return;
    int mid=(first+last)/2;
    MergeSort(str,first,mid,count);
    MergeSort(str,mid+1,last,count);
    Merge(str,first,mid,last,count);
}
int main() {
    int n, m;
    scanf("%d%d", &n, &m);
    auto* DNA=new SortOrder[m];
    for(int i=0;i<m;i++){
        DNA[i].Order=i;
        cin>>DNA[i].str;
        string UseToSort=DNA[i].str;
        MergeSort(UseToSort,0,n-1,DNA[i].Count);
    }
    sort(DNA,DNA+m);
    for(int i=0;i<m;i++){
        printf("%s\n",DNA[i].str.c_str());
    }
}