#include <iostream>
using namespace std;

void insertionSort(int a[], int low, int high) {
    for (int i = low + 1; i <= high; i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= low && a[j] > key) {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
}


void QuickSort(int a[], int low, int high) {
    if (high - low < 10) {
        insertionSort(a, low, high);
        return;
    }

    int i = low;
    int j = high;

    int mid = low + (high - low) / 2;
    int key = a[mid];
    swap(a[low], a[mid]); 

    while (i < j) {
        while (i < j && a[j] >= key) j--;
        a[i] = a[j];
        while (i < j && a[i] <= key) i++;
        a[j] = a[i];
    }
    a[i] = key;

    QuickSort(a, low, i - 1);
    QuickSort(a, i + 1, high);
}

int main() {
    int N;
    cin >> N;
    int a[N];
    for (int i = 0; i < N; i++)
        cin >> a[i];

    QuickSort(a, 0, N - 1);
    cout << a[N / 2];
    return 0;
}
