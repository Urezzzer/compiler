int foo()
{
    return 15;
}

int main() {
    int a = 5;
    int b = 10;
    int c = a + b + foo();
}
