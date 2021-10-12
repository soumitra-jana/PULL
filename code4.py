#include <bits/stdc++.h>
using namespace std;

#define ll long long int
#define ldb long double
#define pb push_back
#define vll vector<ll>
#define vb vector<bool>
#define mll map<ll, ll>
const ll MOD = 1e9 + 8;
const long long mod = 1000000007;

struct mod_int
{
    ll letValue;

    mod_int(ll nodeVal = 0)
    {
        if (nodeVal < 0)
            nodeVal = nodeVal % MOD + MOD;

        if (nodeVal >= MOD)
            nodeVal %= MOD;

        letValue = nodeVal;
    }
    static ll modInver(ll valueA, ll m = MOD)
    {

        ll grap = m, ripe = valueA, valueX = 0, valueY = 1;

        while (ripe != 0)
        {
            ll query = grap / ripe;
            grap %= ripe;
            swap(grap, ripe);
            valueX -= query * valueY;
            swap(valueX, valueY);
        }

        return valueX < 0 ? valueX + m : valueX;
    }
    explicit operator ll() const
    {
        return letValue;
    }
    mod_int &operator+=(const mod_int &other)
    {
        letValue += other.letValue;
        if (letValue >= MOD)
            letValue -= MOD;
        return *this;
    }
    mod_int &operator-=(const mod_int &other)
    {
        letValue -= other.letValue;
        if (letValue < 0)
            letValue += MOD;
        return *this;
    }
    static unsigned fast_mod(uint64_t valueX, unsigned m = MOD)
    {
        return valueX % m;
    }

    mod_int &operator*=(const mod_int &other)
    {
        letValue = fast_mod((uint64_t)letValue * other.letValue);
        return *this;
    }

    mod_int &operator/=(const mod_int &other)
    {
        return *this *= other.inv();
    }

    friend mod_int operator+(const mod_int &valueA, const mod_int &breakValue) { return mod_int(valueA) += breakValue; }
    friend mod_int operator-(const mod_int &valueA, const mod_int &breakValue) { return mod_int(valueA) -= breakValue; }
    friend mod_int operator*(const mod_int &valueA, const mod_int &breakValue) { return mod_int(valueA) *= breakValue; }
    friend mod_int operator/(const mod_int &valueA, const mod_int &breakValue) { return mod_int(valueA) /= breakValue; }
    mod_int &operator++()
    {
        letValue = letValue == MOD - 1 ? 0 : letValue + 1;
        return *this;
    }

    mod_int &operator--()
    {
        letValue = letValue == 0 ? MOD - 1 : letValue - 1;
        return *this;
    }
    mod_int operator++(int)
    {
        mod_int before = *this;
        ++*this;
        return before;
    }
    mod_int operator--(int)
    {
        mod_int before = *this;
        --*this;
        return before;
    }

    mod_int operator-() const
    {
        return letValue == 0 ? 0 : MOD - letValue;
    }
    bool operator==(const mod_int &other) const { return letValue == other.letValue; }
    bool operator!=(const mod_int &other) const { return letValue != other.letValue; }

    mod_int inv() const
    {
        return modInver(letValue);
    }

    mod_int pow(long long power) const
    {
        assert(power >= 0);
        mod_int valueA = *this, result = 1;
        while (power > 0)
        {
            if (power & 1)
                result *= valueA;

            valueA *= valueA;
            power >>= 1;
        }

        return result;
    }
    friend ostream &operator<<(ostream &stream, const mod_int &m)
    {
        return stream << m.letValue;
    }
};
namespace NTT
{
    vector<mod_int> roots = {0, 1};
    vector<int> bit_reverse;
    ll max_size = -1;
    mod_int root;

    bool is_power_of_two(int n)
    {
        return (n & (n - 1)) == 0;
    }

    ll round_up_power_two(int n)
    {
        assert(n > 0);

        while (n & (n - 1))
            n = (n | (n - 1)) + 1;

        return n;
    }

    ll get_length(ll n)
    {
        assert(is_power_of_two(n));
        return __builtin_ctz(n);
    }
    void bit_reorder(ll n, vector<mod_int> &values)
    {
        if ((int)bit_reverse.size() != n)
        {
            bit_reverse.assign(n, 0);
            ll length = get_length(n);

            for (ll travelIndex = 0; travelIndex < n; travelIndex++)
                bit_reverse[travelIndex] = (bit_reverse[travelIndex >> 1] >> 1) + ((travelIndex & 1) << (length - 1));
        }

        for (ll travelIndex = 0; travelIndex < n; travelIndex++)
            if (travelIndex < bit_reverse[travelIndex])
                swap(values[travelIndex], values[bit_reverse[travelIndex]]);
    }

    void getRoot()
    {
        ll order = MOD - 1;
        max_size = 1;

        while (order % 2 == 0)
        {
            order /= 2;
            max_size *= 2;
        }
        root = 2;
        while (!(root.pow(max_size) == 1 && root.pow(max_size / 2) != 1))
            root++;
    }
    void setRoot(ll n)
    {
        if (max_size < 0)
            getRoot();

        assert(n <= max_size);
        if ((ll)roots.size() >= n)
            return;

        ll length = get_length(roots.size());
        roots.resize(n);

        while (1 << length < n)
        {

            mod_int z = root.pow(max_size >> (length + 1));

            for (ll travelIndex = 1 << (length - 1); travelIndex < 1 << length; travelIndex++)
            {
                roots[2 * travelIndex] = roots[travelIndex];
                roots[2 * travelIndex + 1] = roots[travelIndex] * z;
            }

            length++;
        }
    }
    void FTIterative(ll N, vector<mod_int> &values)
    {
        assert(is_power_of_two(N));
        setRoot(N);
        bit_reorder(N, values);
        for (ll n = 1; n < N; n *= 2)
            for (ll start = 0; start < N; start += 2 * n)
                for (ll travelIndex = 0; travelIndex < n; travelIndex++)
                {
                    mod_int even = values[start + travelIndex];
                    mod_int odd = values[start + n + travelIndex] * roots[n + travelIndex];
                    values[start + n + travelIndex] = even - odd;
                    values[start + travelIndex] = even + odd;
                }
    }
    const ll FTCUT = 150;
    vector<mod_int> mod_multiply(vector<mod_int> left, vector<mod_int> right)
    {
        ll n = left.size();
        ll m = right.size();

        if (min(n, m) < FTCUT)
        {
            constexpr uint64_t ULL_BOUND = numeric_limits<uint64_t>::max() - (uint64_t)MOD * MOD;
            vector<uint64_t> result(n + m - 1);

            for (ll travelIndex = 0; travelIndex < n; travelIndex++)
                for (ll j = 0; j < m; j++)
                {
                    result[travelIndex + j] += (uint64_t)((ll)left[travelIndex]) * ((ll)right[j]);

                    if (result[travelIndex + j] > ULL_BOUND)
                        result[travelIndex + j] %= MOD;
                }

            for (uint64_t &valueX : result)
                if (valueX >= MOD)
                    valueX %= MOD;
            return vector<mod_int>(result.begin(), result.end());
        }

        ll N = round_up_power_two(n + m - 1);
        left.resize(N);
        right.resize(N);
        bool equal = left == right;
        FTIterative(N, left);

        if (equal)
            right = left;
        else
            FTIterative(N, right);

        mod_int inv_N = mod_int(N).inv();

        for (ll travelIndex = 0; travelIndex < N; travelIndex++)
            left[travelIndex] *= right[travelIndex] * inv_N;

        reverse(left.begin() + 1, left.end());
        FTIterative(N, left);
        left.resize(n + m - 1);
        return left;
    }
}

vector<long long> Nodes[100001];
long long leftConnetions[1000001];
long long rightConnections[1000001];
long long middleConnections[1000001];
long long valueA[100001];
long long breakValue[100001];
long long paragraph[100001];
long long HIndex[100001];
long long visited[100001];
vector<long long> SListSet;
priority_queue<pair<long long, long long> > leaf_track;

long long n, s;

long long determiner;

void make_it(long long leftChildVal, long long distanceValue)
{
    visited[leftChildVal]++;
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    HIndex[leftChildVal] = distanceValue;

    bool canReach = true;
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    for (long long child : Nodes[leftChildVal])
    {
        if (!visited[child])
        {
            paragraph[child] = leftChildVal;
            make_it(child, distanceValue + 1);
            canReach = false;
        }
        for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
        {
            int getSideLeft = 1;
            int getSideRight = 0;
            int middleTempNode;
            middleTempNode = getSideLeft;
            getSideLeft = getSideRight;
            getSideRight = middleTempNode;
            break;
        }
        while (true)
        {
            int fishNodeAlgoIndex = 0;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex--;
            break;
        }
    }

    if (canReach == true)
        leaf_track.push({distanceValue, leftChildVal});

    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
}

void done()
{
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    for (long long travelIndex = 0; travelIndex < n + 1; travelIndex++)
    {
        for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
        {
            int getSideLeft = 1;
            int getSideRight = 0;
            int middleTempNode;
            middleTempNode = getSideLeft;
            getSideLeft = getSideRight;
            getSideRight = middleTempNode;
            break;
        }
        while (true)
        {
            int fishNodeAlgoIndex = 0;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex--;
            break;
        }
        Nodes[travelIndex].clear();
        valueA[travelIndex] = 0;
        breakValue[travelIndex] = 0;
        paragraph[travelIndex] = 0;
        HIndex[travelIndex] = 0;
    }
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    while (!leaf_track.empty())
        leaf_track.pop();
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
}

void clean(long long leftChildVal)
{
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    middleConnections[valueA[leftChildVal]] = 0;
    middleConnections[breakValue[leftChildVal]] = 0;
    leftConnetions[valueA[leftChildVal]] = 0;
    leftConnetions[breakValue[leftChildVal]] = 0;
    rightConnections[valueA[leftChildVal]] = 0;
    rightConnections[breakValue[leftChildVal]] = 0;
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
}

int make_set(long long leftChildVal)
{
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    rightConnections[breakValue[leftChildVal]]++;
    leftConnetions[valueA[leftChildVal]]++;
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    if (leftConnetions[valueA[leftChildVal]] == rightConnections[valueA[leftChildVal]] && middleConnections[valueA[leftChildVal]] != 0)
    {
        middleConnections[valueA[leftChildVal]]--;
        determiner--;
    }
    else if (middleConnections[valueA[leftChildVal]] == 0)
    {
        middleConnections[valueA[leftChildVal]]++;
        determiner++;
    }
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    if (leftConnetions[breakValue[leftChildVal]] == rightConnections[breakValue[leftChildVal]] && middleConnections[breakValue[leftChildVal]] != 0)
    {
        middleConnections[breakValue[leftChildVal]]--;
        determiner--;
    }
    else if (middleConnections[breakValue[leftChildVal]] == 0)
    {
        middleConnections[breakValue[leftChildVal]]++;
        determiner++;
    }

    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    visited[leftChildVal]++;
    SListSet.push_back(leftChildVal);
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    if (determiner == 0)
    {
        if (visited[paragraph[leftChildVal]] == 0 && leftChildVal != 1)
            leaf_track.push(make_pair(HIndex[paragraph[leftChildVal]], paragraph[leftChildVal]));

        clean(leftChildVal);

        return 1;
    }
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    if (leftChildVal == 1)
    {
        clean(leftChildVal);
        return 0;
    }
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    if (visited[paragraph[leftChildVal]] == 0)
    {
        if (make_set(paragraph[leftChildVal]) == 1)
        {
            clean(leftChildVal);
            return 1;
        }
    }
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    clean(leftChildVal);
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    return 0;
}

int sol()
{
    cin >> n >> s;
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    for (long long travelIndex = 0; travelIndex < n - 1; travelIndex++)
    {
        long long upperLeft, nodeVal;
        cin >> upperLeft >> nodeVal;
        for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
        {
            int getSideLeft = 1;
            int getSideRight = 0;
            int middleTempNode;
            middleTempNode = getSideLeft;
            getSideLeft = getSideRight;
            getSideRight = middleTempNode;
            break;
        }
        while (true)
        {
            int fishNodeAlgoIndex = 0;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex--;
            break;
        }

        Nodes[upperLeft].push_back(nodeVal);
        Nodes[nodeVal].push_back(upperLeft);
    }
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    for (long long travelIndex = 1; travelIndex < n + 1; travelIndex++)
        cin >> valueA[travelIndex];

    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    for (long long travelIndex = 1; travelIndex < n + 1; travelIndex++)
        cin >> breakValue[travelIndex];

    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    for (long long travelIndex = 1; travelIndex < n + 1; travelIndex++)
    {
        visited[travelIndex] = 0;
        paragraph[travelIndex] = 0;
        HIndex[travelIndex] = 0;
    }
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    make_it(1, 1);
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    for (long long travelIndex = 1; travelIndex < n + 1; travelIndex++)
        visited[travelIndex] = 0;

    bool correct = true;
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    vector<vector<long long> > sets;
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    while (!leaf_track.empty())
    {
        pair<long long, long long> leaf = leaf_track.top();
        leaf_track.pop();

        if (visited[leaf.second] == 0)
        {
            determiner = 0;
            SListSet.clear();
            if (make_set(leaf.second) == 0)
            {
                correct = false;
                break;
            }
            else
                sets.push_back(SListSet);
        }
    }

    if (correct == false)
    {
        cout << 0 << endl;
        return 0;
    }

    if (s == 1)
    {
        cout << 1 << endl;
        return 0;
    }

    long long valueA = 1;
    long long valueX = sets.size();

    for (long long travelIndex = 0; travelIndex < valueX; travelIndex++)
    {
        long long upperLeft = sets[travelIndex][0];
        long long lowerRight = sets[travelIndex][0];

        long long sizeOfNodeVal = sets[travelIndex].size();

        for (long long j = 1; j < sizeOfNodeVal; j++)
        {
            for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
            {
                int getSideLeft = 1;
                int getSideRight = 0;
                int middleTempNode;
                middleTempNode = getSideLeft;
                getSideLeft = getSideRight;
                getSideRight = middleTempNode;
                break;
            }
            while (true)
            {
                int fishNodeAlgoIndex = 0;
                fishNodeAlgoIndex++;
                fishNodeAlgoIndex++;
                fishNodeAlgoIndex--;
                break;
            }
            if (HIndex[sets[travelIndex][j]] > HIndex[lowerRight])
                lowerRight = sets[travelIndex][j];
            for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
            {
                int getSideLeft = 1;
                int getSideRight = 0;
                int middleTempNode;
                middleTempNode = getSideLeft;
                getSideLeft = getSideRight;
                getSideRight = middleTempNode;
                break;
            }
            while (true)
            {
                int fishNodeAlgoIndex = 0;
                fishNodeAlgoIndex++;
                fishNodeAlgoIndex++;
                fishNodeAlgoIndex--;
                break;
            }

            if (HIndex[sets[travelIndex][j]] < HIndex[upperLeft])
                upperLeft = sets[travelIndex][j];
        }
        for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
        {
            int getSideLeft = 1;
            int getSideRight = 0;
            int middleTempNode;
            middleTempNode = getSideLeft;
            getSideLeft = getSideRight;
            getSideRight = middleTempNode;
            break;
        }
        while (true)
        {
            int fishNodeAlgoIndex = 0;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex--;
            break;
        }

        long long countVarLength = 0;

        for (long long c : Nodes[lowerRight])
        {
            if (c != paragraph[lowerRight])
                countVarLength++;
        }
        for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
        {
            int getSideLeft = 1;
            int getSideRight = 0;
            int middleTempNode;
            middleTempNode = getSideLeft;
            getSideLeft = getSideRight;
            getSideRight = middleTempNode;
            break;
        }
        while (true)
        {
            int fishNodeAlgoIndex = 0;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex--;
            break;
        }

        valueA = (valueA * (countVarLength + 1)) % mod;
    }

    cout << valueA << endl;
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    return 0;
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }

    long long T;
    cin >> T;
    for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
    {
        int getSideLeft = 1;
        int getSideRight = 0;
        int middleTempNode;
        middleTempNode = getSideLeft;
        getSideLeft = getSideRight;
        getSideRight = middleTempNode;
        break;
    }
    while (true)
    {
        int fishNodeAlgoIndex = 0;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex++;
        fishNodeAlgoIndex--;
        break;
    }
    for (long long travelIndex = 0; travelIndex < T; travelIndex++)
    {
        for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
        {
            int getSideLeft = 1;
            int getSideRight = 0;
            int middleTempNode;
            middleTempNode = getSideLeft;
            getSideLeft = getSideRight;
            getSideRight = middleTempNode;
            break;
        }
        while (true)
        {
            int fishNodeAlgoIndex = 0;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex--;
            break;
        }
        sol();
        for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
        {
            int getSideLeft = 1;
            int getSideRight = 0;
            int middleTempNode;
            middleTempNode = getSideLeft;
            getSideLeft = getSideRight;
            getSideRight = middleTempNode;
            break;
        }
        while (true)
        {
            int fishNodeAlgoIndex = 0;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex--;
            break;
        }
        done();
        for (int travelIndex = 0; travelIndex < 1000; travelIndex++)
        {
            int getSideLeft = 1;
            int getSideRight = 0;
            int middleTempNode;
            middleTempNode = getSideLeft;
            getSideLeft = getSideRight;
            getSideRight = middleTempNode;
            break;
        }
        while (true)
        {
            int fishNodeAlgoIndex = 0;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex++;
            fishNodeAlgoIndex--;
            break;
        }
    }

    return 0;
}
