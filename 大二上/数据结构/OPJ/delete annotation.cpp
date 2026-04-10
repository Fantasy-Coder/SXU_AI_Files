#include<iostream>
using namespace std;
int main(){
    char ch, next_c, last_c='\0';
    bool anno_tag=false;//注释标志
    bool quote_flag=false;//引号标志
    while((ch=getchar())!=EOF){
        if(ch==92){ //'\'的asc码
            next_c=cin.peek();
            if(next_c==34){ //'"'的asc码
                getchar();
                printf("%c%c",ch,next_c);
                continue;
            }
        }
        if(ch=='"'&&!anno_tag) quote_flag=!quote_flag;
        if(ch=='/'&&!quote_flag){
            if(anno_tag){
                if(last_c=='*'){
                    anno_tag=false;
                    last_c=ch;
                    continue;
                }
            }
            else{
                next_c=cin.peek();
                if(next_c=='*'){
                    getchar();
                    anno_tag=true;
                }
            }
        }
        if(!anno_tag) printf("%c",ch);
        last_c=ch;
    }
}