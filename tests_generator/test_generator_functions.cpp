int func1(int a, int b) {
    return a - b;
}

int func2(int a) {
    return a * a;
}

int main() {
    int a = func1(10,3);
    a = func2(a);
}