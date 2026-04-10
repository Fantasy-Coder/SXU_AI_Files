#include"iostream"
#include"iomanip"
#include"fstream"
#include"string.h" 
using namespace std;
int main()
{
	char *name[]={"object1","object2"};
	double price[]={100,90};
	int n;		cout<<"ofstream文本文件使用演示"<<endl;					//使用文件输出流类ofstream的文件对象fp将数据输出到文本文件“price.txt”中 
	ofstream fp;														//文件输出流类ofstream对象fp（自己定义） 
	fp.open("price.txt");												//打开文件“price.txt” 
	fp<<"商品名称 单价 \n"<<setiosflags(ios::left);
	for(n=0;n<2;n++)
	{
		fp<<setw(8)<<name[n];	fp<<" ";
		fp<<setw(6)<<price[n];	fp<<endl;
	}
	fp.close();															//关闭文件 
	
	cout<<endl<<"ofstram二进制文件使用演示"<<endl;
	ofstream fp1;
	fp1.open("price.dat",ios::binary);									//以二进制模式打开文件“price.dat” 
	char str[7];												
	for(n=0;n<2;n++)
	{
		strcpy(str,name[n]);
		fp1.write(str,sizeof(str));										//输出商品名称，用write（输出成员地址，输出的字节数） 
		fp1.write((char*)&price[n],sizeof(double));						//输出价格 
	}
	fp1.close();
	
	cout<<endl<<"ifstream文本文件使用演示"<<endl;
	ifstream fin1;														//使用文件输入流类ifstream的文件对象fin1从文本文件“price.txt”中输入数据 
	char name1[20];
	double price1;
	fin1.open("price.txt");												//打开文件“price.txt” 
	fin1.getline(name1,19);												//读出标题行 
	cout<<name1<<endl;
	for(n=0;n<2;n++)
	{
		fin1>>name1>>price1;											//从文件“price.txt”中读取商品名称和单价 
		cout<<name1<<","<<price1<<endl;									//显示商品名称和单价，验证输入结果 
	}
	fin1.close();
	
	cout<<endl<<"ifstream二进制文件使用演示"<<endl; 
	ifstream fin2;														//使用文件对象fin2从二进制文件“price.dat”中输入数据 
	fin2.open("price.dat",ios::binary);									//以二进制模式打开文件“price.dat” 
	for(n=0;n<2;n++)
	{
		fin2.read(name1,7);												//输入商品名称，用read（变量地址，读出的字节数） 
		fin2.read((char*)&price1,8);									//输入单价
		cout<<name1<<","<<price1<<endl;									//显示商品名称和单价			
	}
	fin2.close();
	
	cout<<endl<<"eof和good使用演示"<<endl;
	ifstream fin("price.txt");
	char ch;
	while(true)
	{
		fin.get(ch);													//从price.txt中读取1个字符 
		if(fin.eof()==true||fin.good()==false)							//eof的返回值，true代表文件已结束，false代表文件未结束 
			{															//godd的返回值，true代表文件正常，false代表文件损坏 
				break;
			}
		cout.put(ch);													//显示所读出的字符ch 
	}
	fin.close();
	
	cout<<endl<<"seekg和tellp使用演示"<<endl;
	fstream fobj;														//定义文件输入/输出流类fstream的文件对象fobj 
	fobj.open("price.dat",ios::in|ios::binary);							//以输入/二进制模式打开文件price.dat
	for(n=0;n<2;n++)
	{
		fobj.read(name1,7);
		fobj.read((char*)&price1,8);
		cout<<name1<<","<<price1<<endl;
	 }
	 fobj.seekg(-15,ios::end);											//读文件指针 istream& seekg(所移动的字节数（可正负），移动的起始位置)  tellg，返回当前读文件指针的位置 
	 fobj.read(name1,7);												//写文件指针 ostream& seekp(所移动的字节数（可正负），移动的起始位置)  tellp，返回当前写文件指针的位置 
	 fobj.read((char*)&price1,8);
	 cout<<"前一行"<<endl; 
	 cout<<name1<<","<<price1<<endl;
	 int a;
	 a=fobj.tellg();
	 cout<<"文件指针的当前位置为"<<a<<endl; 
	 fobj.close();
	 cout<<"关闭文件"<<endl; 
}