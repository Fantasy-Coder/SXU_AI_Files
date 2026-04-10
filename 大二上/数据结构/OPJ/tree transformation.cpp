#include<iostream>
#include<cmath>
#include<stack> 
using namespace std;

int main()
{
    int cnt = 0;
    char t[1000000];
    while (cin >> t)
    {
        if (t[0] == '#')
            break;
        int nh = 0, h = 0, nh2 = 0, h2 = 0; 
        stack<int> now;
        now.push(0);
        
        for (int i = 0; t[i] != '\0'; i++)
        {
            if (t[i] == 'd')
            {
                nh++; 
                nh2++;
                now.push(nh2);
            }
            else if (t[i] == 'u')
            {
                if (!now.empty())
                {
                    nh--;
                    nh2 = now.top();
                    now.pop();
                }
            }

            h2 = max(h2, nh2);
            h = max(h, nh);
        }
        cout << "Tree " << ++cnt << ": " << h << " => " << h2 << endl;  
    }
    return 0;
}