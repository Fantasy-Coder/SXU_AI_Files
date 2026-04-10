#include"iostream"
#include"vector" 
#include"algorithm"
using namespace std;
int main()
{
	cout<<"向量类vector演示"<<endl; 
	vector<int> x;//定义1个int型数据集合x
	for(int n=0;n<5;n++)//添加5个向量元素 
	{
		x.push_back(n*n);//第n个元素的值等于n的平方 
	}
	vector<int>::iterator p;//定义1个向量类的容器迭代器p 
	cout<<"向量中的内容为：";
	for(p=x.begin();p<x.end();p++)//通过容器迭代器p遍历向量 
	{
		cout<<*p<<",";
	}
	cout<<endl;
	cout<<"向量中元素的个数为"<<x.size()<<endl;
	x.pop_back();//删除向量中的最后一个元素，再显示其中的元素个数 
	cout<<"size="<<x.size()<<endl;
	
	cout<<endl<<"排序演示"<<endl;
	vector<int> x1;
	vector<int>::iterator p1;
	x1.push_back(3),x1.push_back(7),x1.push_back(9),x1.push_back(5);//添加4个向量元素 
	cout<<"原向量元素："; 
	for(p1=x1.begin();p1<x1.end();p1++)
	{
		cout<<*p1<<",";
	}
	sort(x1.begin(),x1.end());//使用算法函数sort对向量x1进行排序，排序区间为整个向量 
	cout<<endl<<"排序后向量元素：";
	for(p1=x1.begin();p1<x1.end();p1++)
	{
		cout<<*p1<<",";
	}
}