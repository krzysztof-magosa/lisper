#include <string>
#include <fstream>
#include <iostream>

class lexer {
  public:
  lexer(std::istream& stream);
  next_token();

  protected:
  std::istream& stream;
};

lexer::lexer(std::istream& stream) : stream(stream) {
}

int main() {
  std::ifstream stream;
  stream.open("test.lisper");

  lexer l(stream);

  return 0;
}
