# include <cstdio>
# include <cstring>
# include <algorithm>
using namespace std;
int cnt;
int a[1000];
struct node{
	int data;
	node *l, *r;
};
node *newnode(){
	node *t;
	t=(node *)malloc(sizeof(node));
	t->l=t->r=NULL;
	return t;
}

void jianshu(node *T, int d){
	if(d>T->data)
    {
		if(!T->r)
        {
			T->r=newnode();
			T->r->data=d;
			return;
		}
		else
        {
			jianshu(T->r, d);
		}
	}
    
	else if(d<T->data)
    {
		if(!T->l)
        {
			T->l=newnode();
			T->l->data=d;
			return;
		}
		else
        {
			jianshu(T->l, d);
		}
	}
	else
	return;
}


void qianxubianli(node *T){
	if(T){
		a[cnt++]=T->data;
		qianxubianli(T->l);
		qianxubianli(T->r);
	}
}
int main(){
	char flage;
	int num, i;
	node *T;
	T=newnode();
	scanf("%d", &num);
	flage=getchar();
	T->data=num;
	while(flage==' '){
		scanf("%d", &num);
		jianshu(T, num);
		flage=getchar();
	}
	cnt=0;
	qianxubianli(T);
    for(i=0; i<=cnt-1; i++){
    	if(i!=cnt-1){
    		printf("%d ", a[i]);
		}
		else{
			printf("%d", a[i]);
		}
	}
	return 0;
}