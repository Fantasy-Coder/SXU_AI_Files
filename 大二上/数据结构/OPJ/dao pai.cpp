#include <iostream>
#include <algorithm>
#include <string>
using namespace std;
int n, m;
string file[1003][103];
string tmp;
int num[1005];
int main()
{
   
    cin >> n;
    for (int i = 0; i < n; i++)
    {
        cin >> num[i];
        for (int j = 0; j < num[i]; j++)
        {
            cin >> file[i][j];
        }
    }
    cin >> m;
    while(m--)
    {
        cin >> tmp;
        int flag = 0;
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < num[i]; j++)
            {
                if (file[i][j] == tmp)
                {
                    cout << i + 1 << ' ';
                    flag = 1;
                    break;
                }
            }
        }
        if(!flag)
            cout << "NOT FOUND";
        cout << endl;
    }
    return 0;
}
