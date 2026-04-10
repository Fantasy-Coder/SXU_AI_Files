#include"iostream"
using namespace std;
int main()
{
	int row,line,i,j,**p;
	cin>>row>>line;
	p=new int*[row];			//先给每一行分配内存 
	for(i=0;i<row;i++)
	{
		p[i]=new int[line];		//再给每一行的每个元素分配内存 
	}
	cout<<"***";
	for(i=0;i<row;i++)
	{
		for(j=0;j<line;j++)
		{
			cin>>p[i][j];
		}
	}
	for(i=0;i<row;i++)
	{
		for(j=0;j<line;j++)
		{
			cout<<p[i][j]<<"	";
		}
		cout<<endl;
	}
	for(i=0;i<row;i++)
	{
		delete []p[i];			//先释放每一行每个元素的额内存 
	}
	delete []p;					//再释放总体的内存 
}