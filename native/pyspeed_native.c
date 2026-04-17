#include <stddef.h>

#ifdef _WIN32
#define PY_SPEED_EXPORT __declspec(dllexport)
#else
#define PY_SPEED_EXPORT
#endif

PY_SPEED_EXPORT double transform_sum(const double *values, size_t length) {
    double total = 0.0;
    for (size_t i = 0; i < length; ++i) {
        double value = values[i];
        total += (value * value * 1.5) + (value / 3.0) - 7.0;
    }
    return total;
}
