int func(int a, int b)
{
    int c = a + b;
    return c;
}

int main()
{
    int n = 1;
    int k = 2;
    bool flag = true;
    std::string phrase = "Hello";
    if (flag == true)
    {
        if (n <= 1) {
            n = func(n, 2);
        }
    }
    else
    {
        if (k > 1){
            k = func(k,n);
        }
    }
    int c = k * n;
    while (c != 10){
        c = c + 1;
    }
    return 0;
}