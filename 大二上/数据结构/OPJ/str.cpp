#include <iostream>
#include <string>

using namespace std;
string insertSubstring(const string& str, const string& substr) {
    int p = 0; 
    for (int i = 0; i < str.size(); ++i) {
        if (str[i] > str[p]) {
            p = i;
        }
    }
    return str.substr(0, p + 1) + substr + str.substr(p + 1);
}

int main() {
    string str, substr;
    while (cin >> str >> substr) {
        if (substr.size() != 3) {
            cout << "Error: substr must have exactly 3 characters." << endl;
            continue;
        }
        cout << insertSubstring(str, substr) << endl;
    }
    return 0;
}