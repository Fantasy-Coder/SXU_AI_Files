#include <iostream>
#include <algorithm>
#include <map>
#include <string>
#include <cstring>
using namespace std;

map<string,int> addrname;
int len[40][40];
int path[40][40] = { 0 };
int flen[40][40];          //记录原始长度

int main()
{
 int p, q, r;
 cin >> p;
 string name;
 for (int i = 1; i <= p; i++)
  for (int j = 1; j <= p; j++)
  {
   if (i == j)
   {
    len[i][j] = 0;
    path[i][j] = i;
   }
   else
   {
    len[i][j] = 9999;
    path[i][j] = -1;
   }
  }
 for (int i = 1; i <= p; i++)
 {
  cin >> name;
  addrname.insert(make_pair(name, i));
 }
 cin >> q;
 string v1, v2;
 int dis;
 while (q--)
 {
  cin >> v1 >> v2;
  cin >> dis;
  len[addrname[v1]][addrname[v2]] = dis;
  flen[addrname[v1]][addrname[v2]] = dis;
  path[addrname[v1]][addrname[v2]] = addrname[v1];
  len[addrname[v2]][addrname[v1]] = dis;
  flen[addrname[v2]][addrname[v1]] = dis;
  path[addrname[v2]][addrname[v1]] = addrname[v2];
 }
 for (int v = 1; v <= p; v++)
 {
  for (int i = 1; i <= p; i++)
   for (int j = 1; j <= p; j++)
   {
    if (len[i][v] + len[v][j] < len[i][j])
    {
     len[i][j] = len[i][v] + len[v][j];
     path[i][j] = path[v][j];
    }
   }
 }
 cin >> r;
 while (r--)
 {
  string b, e;
  cin >> b >> e;
  while (b != e)
  {
   cout << b << "->(";
   cout << flen[addrname[b]][path[addrname[e]][addrname[b]]] << ")->";
   map<string, int>::iterator p = addrname.begin();
   for (p; p != addrname.end(); ++p)
   {
    if (p->second == path[addrname[e]][addrname[b]])
    {
     b = p->first;
     break;
    }
   }
  }
  cout << e << endl;
 }
 return 0;
}