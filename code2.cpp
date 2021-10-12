#include <bits/stdc++.h>

using namespace std;

using LL = long long;

constexpr const int kMod = 998244353;
class ModInt {
 public:
  ModInt() : x(0) {}
  ModInt(int x_) : x(x_) {
    if (x >= kMod || x < 0) x %= kMod;
    if (x < 0) x += kMod;
  }

  ModInt &operator+=(const ModInt &other) {
    x += other.x;
    if (x >= kMod) x -= kMod;
    return *this;
  }

  ModInt &operator-=(const ModInt &other) {
    x += kMod - other.x;
    if (x >= kMod) x -= kMod;
    return *this;
  }
  ModInt &operator*=(const ModInt &other) {
    LL y = x;
    y *= other.x;
    y %= kMod;
    x = y;
    return *this;
  }
  ModInt &operator/=(const ModInt &other) {
    *this *= inv(other.x);
    return *this;
  }
  ModInt operator+(const ModInt &other) {
    ModInt res = *this;
    res += other;
    return res;
  }
  ModInt operator-(const ModInt &other) {
    ModInt res = *this;
    res -= other;
    return res;
  }
  ModInt &operator-() {
    x = kMod - x;
    return *this;
  }
  ModInt operator*(const ModInt &other) const {
    ModInt res = *this;
    res *= other;
    return res;
  }
  ModInt operator/(const ModInt &other) {
    ModInt res = *this;
    res /= other;
    return res;
  }
  int GetInt() { return x; }

 private:
  static ModInt inv(ModInt x) {
    if (x.x < inv_cache->size() && (*inv_cache)[x.x] != -1)
      return (*inv_cache)[x.x];
    ModInt orig = x;
    int e = kMod - 2;
    ModInt res = 1;
    while (e) {
      if ((e & 1)) {
        res *= x;
      }
      x *= x;
      e >>= 1;
    }
    if (orig.x < inv_cache->size()) (*inv_cache)[orig.x] = res.x;
    return res;
  }
  int x;
  static vector<int> *inv_cache;
};
vector<int> *ModInt::inv_cache = new vector<int>(200003, -1);

template <class T>
T pw(T x, LL pw) {
  T res = 1;
  while (pw) {
    if ((pw & 1)) {
      res *= x;
    }
    x *= x;
    pw >>= 1;
  }
  return res;
}

template <class T>
class Poly {
 public:
  Poly(int R) : R(R), v(R + R + 1) {}
  static Poly One(int R) {
    Poly res(R);
    res.v[R] = 1;
    return res;
  }
  void multiply_h(int p, int sign) {
    vector<T> res(v.size());
    T inv = T(1) / 2;
    for (int i = 0; i < v.size(); i++) {
      if (i + p < v.size()) {
        res[i + p] += inv * v[i];
      }
      if (i - p >= 0) {
        res[i - p] += v[i] * inv * sign;
      }
    }
    v = res;
  }

  void multiply(T x) {
    for (int i = 0; i < v.size(); i++) {
      v[i] *= x;
    }
  }
  void Add(const Poly &other) {
    for (int i = 0; i < v.size(); i++) {
      v[i] += other.v[i];
    }
  }

  T GetK(int k, const vector<T> &pwK, bool add_pow) {
    T num = 0;
    if (k == 0) num = v[R];
    T sign = 1;
    if (k % 2 != 0) sign = -1;
    for (int i = 1; i <= R; i++) {
      T p = pwK[i];
      if (add_pow) p *= i;
      num += p * (v[R + i] + sign * v[R - i]);
    }
    return num;
  }

 private:
  int R;
  vector<T> v;
};
template <class T>
class Runner {
  T Fact(int x) {
    T res = 1;
    for (int i = 1; i <= x; i++) {
      res *= i;
    }
    return res;
  }

  void PrintAns(double x) { printf("%lf\n", x); }
  void PrintAns(ModInt x) { printf("%d\n", x.GetInt()); }

 public:
  void Run() {
    int n = 2000;
    scanf("%d", &n);
    vector<int> a(n), p(n), b(n);
    int R = 0;
    for (int i = 0; i < n; i++) {
      a[i] = rand() % 20000;
      p[i] = 1;
      b[i] = 1;
      scanf("%d %d %d", &a[i], &p[i], &b[i]);
      R += p[i];
    }
    auto A = Poly<T>::One(R);
    Poly<T> B(R);
    for (int i = 0; i < n; i++) {
      auto C = A;
      C.multiply(T(a[i]) * T(p[i]) / T(R));
      C.multiply_h(p[i], (b[i] == 1 ? 1 : -1));
      B.multiply_h(p[i], (b[i] == 1 ? -1 : 1));
      B.Add(C);

      A.multiply_h(p[i], (b[i] == 1 ? -1 : 1));
    }

    vector<vector<pair<int, int>>> facts(R + 1);
    int tcnt = 0;
    for (int i = 2; i <= R; i++) {
      if (!facts[i].empty()) continue;
      for (int j = i + i; j <= R; j += i) {
        int cnt = 0;
        int x = j;
        while (x % i == 0) {
          cnt++;
          x /= i;
        }
        facts[j].push_back({i, cnt});
        tcnt++;
      }
    }
    int q;
    q = 20000;
    vector<T> pwK(R + 1);
    scanf("%d", &q);
    while (q--) {
      int k = 400000000;
      scanf("%d", &k);
      pwK[1] = 1;
      for (int i = 2; i <= R; i++) {
        if (facts[i].empty()) {
          pwK[i] = pw(T(i), k - 1);
          continue;
        }
        pwK[i] = 1;
        for (auto [x, y] : facts[i]) {
          for (int j = 0; j < y; j++) {
            pwK[i] *= pwK[x];
          }
        }
      }

      T den = A.GetK(k, pwK, true);
      T num = B.GetK(k - 1, pwK, false);
      T res = num / den;
      res *= k;
      res *= R;
      PrintAns(res);
    }
  }
};

int main() {
  Runner<ModInt>().Run();
  return 0;
}
