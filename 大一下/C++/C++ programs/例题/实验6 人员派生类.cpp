//从人员类派生出student(学生)类，添加属性：班号 char classNo[7];
//从people类派生出teacher类，添加属性：职务 char principalship[11]、部门char department[21]
//从student类中派生出graduate(研究生)类，添加属性:专业 char subject[21]、导师teacher adviser;
//从graduate类和teacher类派生出TA(助教生)类，注意虚基类的使用。重载相应的成员函数，测试这些类
#include <iostream>
#include <cstring>
using namespace std;
class People
{
private:
    char name[11];
    char number[20];
    char sex[5];
    char id[20];
    static int peoplenum;
public:
    static int getpeoplenum();
    People();
    People(char *_name, char *_number,char *_sex,char* _id);
    void setid(char &_id){strcpy(id,&_id);}
    void setnumber(char &_number){strcpy(number,&_number);}
    void setsex(char &_sex){strcpy(sex,&_sex);}
    void setname(char &_name){strcpy(name,&_name);}
    char *getname(){return name;}
    char *getnumber(){return number;}
    char *getsex(){return sex;}
    char *getid(){return id;}
};
int People::peoplenum = 0;
int People::getpeoplenum(){
    return peoplenum;
}
People::People(){
    strcpy(name,"八红");
    strcpy(number," 000000000000 ");
    strcpy(sex," 男 ");
    strcpy(id,"000000000000000000");
}
People::People(char *_name, char *_number,char *_sex,char* _id){
    strcpy(name,_name);
    strcpy(number,_number);
    strcpy(sex,_sex);
    strcpy(id,_id);
}

class student:virtual public People
{
private:
    char classNo[7];
public:
	student(char *_name, char *_number,char *_sex,char* _id,char *_classNo):People(_name,_number,_sex,_id)
	{
		strcpy(classNo,_classNo);
	}
	student(char *_classNo)
	{
	  strcpy(classNo,_classNo);
	}
	char *getclassNo(){return classNo;}
};

class teacher:virtual public People
{
private:
	char principalship[11];
	char department[21];
public:
	teacher(char *_name, char *_number,char *_sex,char* _id,char *_principalship,char *_department):People(_name,_number,_sex,_id)
	   {
	   		strcpy(principalship,_principalship);
	    	strcpy(department,_department);
	   }
	teacher(char *_principalship,char *_department)
		{
			strcpy(principalship,_principalship);
	    	strcpy(department,_department);
		}
	teacher(teacher &teacher):People(teacher.getname(),teacher.getnumber(),teacher.getsex(),teacher.getid())
    {
		strcpy(principalship,teacher.principalship);
		strcpy(department,teacher.department);
	}
	char *getprincipalship(){return principalship;}
	char *getdepartment(){return department;}
};

class graduate:public student
{
private:
	char subject[21];
  	teacher adviser;
public:
   graduate(char *_name, char *_number,char *_sex,char* _id,char *_classNo,char *_subject,teacher &_adviser):People(_name,_number,_sex,_id),student(_classNo),adviser(_adviser)
      {
	  	strcpy(subject,_subject);
	  }
 	graduate(char *_classNo,char *_subject,teacher &_adviser):student(_classNo),adviser(_adviser)
	{
		strcpy (subject,_subject);
	}
   char *getsubject(){return subject;}
   teacher &getadviser(){return adviser;}
};

class TA:public graduate,public teacher
{
  TA(char *_name, char *_number,char *_sex,char* _id,char *_classNo, char *_subject,teacher &_adviser,char *_principalship,char *_department):People(_name,_number,_sex,_id),teacher(_principalship,_department),graduate(_classNo,_subject,_adviser){}
};

int main()
{
    People *p;
    People pp[5] = {People("小米"," 201701001001 "," 女 ","140429199901018764 "),
                    People("小李"," 201701001002 "," 男 ","140429199905086745 "),
                    People("小林"," 201701001003 "," 女 ","140429199910103947 "),
                    People("小强"," 201701001004 "," 男 ","140429199906074737 "),
                    };
    p = new People[4];
    for(int i = 0 ; i< 5 ; i++)
    {
        cout << pp[i].getname() << "\t" << pp[i].getnumber() << pp[i].getsex()<<
                pp[i].getid() << endl;
    }
	teacher t1("胖子"," 201701001060 "," 女 ","140429197701010000","c++","文艺部");
	graduate g1("梁雪"," 201701001087 "," 女 ","140429199900000000 "," 1703班 "," 计算机 ",t1);
	cout<<g1.getname()<<g1.getnumber()<<g1.getsex()<<g1.getid()<<g1.getclassNo()<<g1.getsubject()<<g1.getadviser().getname()<<endl;
	cout<<t1.getid()<<endl;
    system("pause");
    return 0;
}