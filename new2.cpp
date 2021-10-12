#include <iostream>
#include <unordered_map>
#include <vector>
#include <cassert>
#include <cmath>
#include <memory>

#define ALL_TC int num_tc_5xu8; std::cin >> num_tc_5xu8; while (num_tc_5xu8--)
#define READ_ARRAY(a, n) for (int i = 0; i < n; i++) std::cin >> a[i]
#define READ_INT_ARRAY(a, n) int a[n]; READ_ARRAY(a, n)
#define READ_LONG_ARRAY(a, n) long long a[n]; READ_ARRAY(a, n)
#define READ_INT(x) int x; std::cin >> x
#define READ_LONG(x) long long x; std::cin >> x
#define READ2_INT(x, y) int x, y; std::cin >> x >> y
#define READ2_LONG(x, y) long long x, y; std::cin >> x >> y
#define READ3_INT(x, y, z) int x, y, z; std::cin >> x >> y >> z
#define READ3_LONG(x, y, z) long long x, y, z; std::cin >> x >> y >> z
#define READ_STRING(x) std::string x; std::cin >> x;
#define FL(i, n) for (int i = 0; i < n; i++)

constexpr long modp = 998244353;

using std::vector;
using std::unordered_map;

using Key = std::pair<int, int>;

// first_one_bit_map[i] stores the distance of first one bit from right side.
// Undefined for number 0.
// 000001 -> 1
// 000101 -> 3
// 001111 -> 4
// 000011 -> 2
int first_one_bit_map[256];

void InitFirstOneBitMap() {
  for (int i = 1, j = 0; i < 256 ;i++) {
    if (i >= (1 << j)) {
      j++;
    }
    first_one_bit_map[i] = j;
  }
}


struct PowerFactory {
  void Init(long base) {
    long base_p[32];  // base_p[i] stores base^(2^i)
    for (int i = 0; i < 32; i++) {
      if (i == 0) {
        base_p[i] = base;
      } else {
        base_p[i] = (base_p[i-1] * base_p[i-1]) % modp;
      }
    }
    std::pair<int, long*> pp[4] = {{0, a0}, {8, a1}, {16, a2}, {24, a3}};
    for (auto& x : pp) {
      auto a = x.second;
      int offset = x.first;
      for (int i = 0; i < 256; i++) {
        if (i == 0) {
          a[i] = 1;
        } else {
          a[i] = (base_p[offset + first_one_bit_map[i] - 1] * a[i - (1 << (first_one_bit_map[i] - 1))] ) % modp;
        }
      }
    }
  }
  long get(int n) {
    int e0 = (n & 0xff);
    int e1 = ((n >> 8) & 0xff);
    int e2 = ((n >> 16) & 0xff);
    int e3 = ((n >> 24) & 0xff);
    return (((((a0[e0] * a1[e1]) % modp) * a2[e2] ) % modp) * a3[e3] ) % modp;
  }
  // ao[i] stores base^i
  long a0[256];
  // a1[i] stores (base^i)^(2^8)
  long a1[256];
  // a2[i] stores (base^i)^(2^16)
  long a2[256];
  // a3[i] stores (base^i)^(2^24)
  long a3[256];
};


struct Hasher {
  std::size_t operator()(const Key& k) const {
    return k.first + k.second * 10000;;
  }
};

using Map = unordered_map<Key, long, Hasher>;

long inverse(long a) {
  long t = 0, newt = 1;
  long r = modp, newr = a;
  while (newr != 0) {
    auto quotient = r / newr;
    auto oldt = newt;
    newt = t - quotient * newt;
    t = oldt;
    auto oldr = newr;
    newr = r - quotient * newr;
    r = oldr;
  }



  assert(r <= 1);
  if (t < 0) {
    t += modp;
  }
  return t;
}

long power(long a, int b) {
  long answer = 1;
  long two_power = a;
  for (;b > 0; b /= 2) {
    if (b % 2 == 1) {
      answer *= two_power;
      answer %= modp;
    }
    two_power = (two_power * two_power) % modp;
  }
  return answer;
}

template<typename T>
void print_map(const T& map) {
  std::cout << "{\n";
  for (auto& item: map) {
    std::cout << " " << item.first << " : " << item.second << ",\n";
  }
  std::cout << "}\n";
}

template<typename T>
void print_map2(const T& map) {
  std::cout << "{\n";
  for (auto& item: map) {
    std::cout << " (" << item.first.first << ", '" << item.first.second << "') : " << item.second << ",\n";
  }
  std::cout << "}\n";
}

int TestPower() {
  PowerFactory f;
  f.Init(7);
  for (int i : {1000, 10000, 100000, 10000000}) {
    std::cout << "7^" << i << " = " << f.get(i) << ". Expected = " << power(7, i) << std::endl;
    assert(f.get(i) == power(7, i));
  }
  return 0;
}

int main() {
  InitFirstOneBitMap();
  // return TestPower();
  int n;
  std::cin >> n;
  vector<int> p(n);
  vector<int> b(n);
  vector<long> a(n);
  for (int i = 0; i < n; i++) {
    std::cin >> a[i] >> p[i] >> b[i];
  }
  int q;
  std::cin >> q;
  Map sum_map, count_map;
  sum_map[{p[0], 0}] = (a[0] * p[0]) % modp;
  count_map[{p[0], 0}]++;
  for (int i = 1; i < n; i++) {
    Map new_sum_map, new_count_map;
    for (auto& item : sum_map) {
      auto pos_key = item.first.first + p[i];
      auto neg_key = item.first.first - p[i];
      long count = count_map[item.first];
      auto val = (((a[i] * p[i] ) % modp) * count) % modp;
      Key k1 = {pos_key, item.first.second};
      Key k2 = {neg_key, b[i] ^ item.first.second};
      new_sum_map[k1] += (item.second + val);
      new_sum_map[k2] += (item.second - val);
      new_sum_map[k1] %= modp;
      new_sum_map[k2] %= modp;
      new_count_map[k1] += count;
      new_count_map[k2] += count;
      new_count_map[k1] %= modp;
      new_count_map[k2] %= modp;
    }
    sum_map = std::move(new_sum_map);
    count_map = std::move(new_count_map);
  }
  // print_map2(count_map);
  // print_map2(sum_map);
  // std::cout << "---" << std::endl;
  unordered_map<int, long> sum_map2;
  unordered_map<int, long> count_map2;
  for (auto& item : sum_map) {
    sum_map2[item.first.first] += (item.first.second ? -1 : 1) * item.second;
    sum_map2[item.first.first] %= modp;
  }
  for (auto& item : count_map) {
    count_map2[item.first.first] += (item.first.second ? -1 : 1) * item.second;
    count_map2[item.first.first] %= modp;
  }
  unordered_map<int, std::unique_ptr<PowerFactory>> power_factory_map;
  for (auto& item : count_map2) {
    power_factory_map[item.first] = std::make_unique<PowerFactory>();
    power_factory_map.at(item.first)->Init(item.first);
  }
  // print_map(count_map2);
  // print_map(sum_map2);
  // std::cout << "---" << std::endl;
  int k;


  for (int i = 0; i < q; i++) {
    std::cin >> k;
    long a = 0, b = 0;
    for (auto& item : count_map2) {
      // a += (power(item.first, k-1) * sum_map2.at(item.first)) % modp;
      // b += (power(item.first, k) * item.second) % modp;
      auto x = power_factory_map.at(item.first)->get(k-1);
      a += (x * sum_map2.at(item.first)) % modp;
      b += (((x * item.first) % modp ) * item.second) % modp;
      a %= modp;
      b %= modp;
    }
    a %= modp;
    b %= modp;
    a *= k;
    a %= modp;
    a = (a + modp) % modp;
    b = (b + modp) % modp;
    if (b ==0) b = 1;
    // std::cout << "k = " << k << ", a = " << a << ", b = " << b << std::endl;
    std::cout << (a * inverse(b))%modp << "\n";
  }
  return 0;
}
