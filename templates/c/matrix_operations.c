/*
 * Matrix Operations
 * Complete matrix math library with operations and display.
 * Author: Jay Singh (iamjaysingh)
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX 10

typedef struct {
    int rows, cols;
    double data[MAX][MAX];
} Matrix;

Matrix create_matrix(int rows, int cols) {
    Matrix m;
    m.rows = rows;
    m.cols = cols;
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            m.data[i][j] = 0;
    return m;
}

void print_matrix(const char* name, Matrix *m) {
    printf("\n  %s (%dx%d):\n", name, m->rows, m->cols);
    for (int i = 0; i < m->rows; i++) {
        printf("  │");
        for (int j = 0; j < m->cols; j++) {
            printf(" %7.2f", m->data[i][j]);
        }
        printf(" │\n");
    }
}

Matrix add(Matrix *a, Matrix *b) {
    Matrix result = create_matrix(a->rows, a->cols);
    for (int i = 0; i < a->rows; i++)
        for (int j = 0; j < a->cols; j++)
            result.data[i][j] = a->data[i][j] + b->data[i][j];
    return result;
}

Matrix subtract(Matrix *a, Matrix *b) {
    Matrix result = create_matrix(a->rows, a->cols);
    for (int i = 0; i < a->rows; i++)
        for (int j = 0; j < a->cols; j++)
            result.data[i][j] = a->data[i][j] - b->data[i][j];
    return result;
}

Matrix multiply(Matrix *a, Matrix *b) {
    Matrix result = create_matrix(a->rows, b->cols);
    for (int i = 0; i < a->rows; i++)
        for (int j = 0; j < b->cols; j++)
            for (int k = 0; k < a->cols; k++)
                result.data[i][j] += a->data[i][k] * b->data[k][j];
    return result;
}

Matrix transpose(Matrix *m) {
    Matrix result = create_matrix(m->cols, m->rows);
    for (int i = 0; i < m->rows; i++)
        for (int j = 0; j < m->cols; j++)
            result.data[j][i] = m->data[i][j];
    return result;
}

Matrix scalar_multiply(Matrix *m, double scalar) {
    Matrix result = create_matrix(m->rows, m->cols);
    for (int i = 0; i < m->rows; i++)
        for (int j = 0; j < m->cols; j++)
            result.data[i][j] = m->data[i][j] * scalar;
    return result;
}

double determinant_2x2(Matrix *m) {
    return m->data[0][0] * m->data[1][1] - m->data[0][1] * m->data[1][0];
}

double trace(Matrix *m) {
    double sum = 0;
    int min = m->rows < m->cols ? m->rows : m->cols;
    for (int i = 0; i < min; i++)
        sum += m->data[i][i];
    return sum;
}

int is_symmetric(Matrix *m) {
    if (m->rows != m->cols) return 0;
    for (int i = 0; i < m->rows; i++)
        for (int j = 0; j < m->cols; j++)
            if (fabs(m->data[i][j] - m->data[j][i]) > 1e-9) return 0;
    return 1;
}

Matrix identity(int n) {
    Matrix m = create_matrix(n, n);
    for (int i = 0; i < n; i++)
        m.data[i][i] = 1.0;
    return m;
}

int main() {
    printf("==================================================\n");
    printf("  📐 Matrix Operations\n");
    printf("==================================================\n");

    // Create matrices
    Matrix a = create_matrix(3, 3);
    double vals_a[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            a.data[i][j] = vals_a[i][j];

    Matrix b = create_matrix(3, 3);
    double vals_b[3][3] = {{9, 8, 7}, {6, 5, 4}, {3, 2, 1}};
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            b.data[i][j] = vals_b[i][j];

    print_matrix("Matrix A", &a);
    print_matrix("Matrix B", &b);

    // Operations
    Matrix sum = add(&a, &b);
    print_matrix("A + B", &sum);

    Matrix diff = subtract(&a, &b);
    print_matrix("A - B", &diff);

    Matrix prod = multiply(&a, &b);
    print_matrix("A × B", &prod);

    Matrix trans = transpose(&a);
    print_matrix("Transpose(A)", &trans);

    Matrix scaled = scalar_multiply(&a, 2.0);
    print_matrix("2 × A", &scaled);

    // Properties
    printf("\n  📊 Properties of A:\n");
    printf("    Trace:     %.2f\n", trace(&a));
    printf("    Symmetric: %s\n", is_symmetric(&a) ? "Yes ✅" : "No ❌");

    // 2x2 determinant demo
    Matrix small = create_matrix(2, 2);
    small.data[0][0] = 3; small.data[0][1] = 8;
    small.data[1][0] = 4; small.data[1][1] = 6;
    print_matrix("2x2 Matrix", &small);
    printf("    Determinant: %.2f\n", determinant_2x2(&small));

    // Identity
    Matrix id = identity(3);
    print_matrix("Identity(3)", &id);

    printf("\n  👋 Done!\n");
    return 0;
}
