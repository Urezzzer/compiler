int foo() {
    return 4;
}

std::string bar() {
    return foo();
}

int main() {
    int a = foo() + bar();
}
