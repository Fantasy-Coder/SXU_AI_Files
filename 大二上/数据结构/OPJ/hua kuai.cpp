#include<iostream>
using namespace std;
typedef long long ll;
const int N=1e6+10;
int a[N],q[N];
int n,k;
int main()
{
	cin>>n>>k;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}

	int h=0,t=-1;
	for(int i=1;i<=n;i++){
		if(t>=h&&q[h]<i-k+1) h++;
		while(t>=h&&a[i]<=a[q[t]]) t--; 
		q[++t]=i;
		if(i>=k)
			printf("%d ",a[q[h]]);
	}
	printf("\n");
 
	h=0,t=-1;
	for(int i=1;i<=n;i++){

		if(h<=t&&q[h]<i-k+1) 
			h++;

		while(h<=t&&a[i]>=a[q[t]])
			t--;

		q[++t]=i;

		if(i>=k)
			printf("%d ",a[q[h]]); 
	}
	return 0;
}