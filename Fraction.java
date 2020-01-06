public class Fraction {
    private int num, den;

    public Fraction(int u_num, int u_den){
        if (u_den == 0) {
            throw new IllegalArgumentException("Denominator can't be zero.");
        }
        else{ this.den = u_den;}
        this.num = u_num;

        if (this.den < 0 && this.num > 0 || this.den < 0 && this.num < 0) {
            this.den = this.den * -1;
            this.num = this.num * -1;
        }
    }

    public Fraction (int u_num) {
        this.num = u_num;
        this.den = 1;
    }

    public Fraction() {
        this.num = 0;
        this.den = 1;
    }

    public int getNumerator() { return this.num; }
    public int getDenominator() { return this.den; }

    public String toString() { return this.num + "/" + this.den; }

    public double toDouble() { return ((double) this.num/ (double) this.den); }

    public Fraction add(Fraction other) {
        if (this.den == other.den) {
            return new Fraction((this.num + other.num), this.den);
        }
        else {
            int newNum1 = this.num * other.den;
            int newNum2 = this.den * other.num;
            return new Fraction(newNum1 + newNum2, (this.den * other.den));
        }
    }

    public Fraction subtract(Fraction other) {
        if (this.den == other.den) {
            return new Fraction((this.num - other.num), this.den);
        }
        else {
            int newNum1 = this.num * other.den;
            int newNum2 = this.den * other.num;
            return new Fraction(newNum1 - newNum2, (this.den * other.den));
        }
    }

    public Fraction multiply(Fraction other) { return new Fraction((this.num * other.num), (this.den * other.den)); }

    public Fraction divide(Fraction other) {
        if (other.den == 0) {
            throw new IllegalArgumentException("Denominator can't be 0.");
        }
        return new Fraction((this.num * other.den), (this.den * other.num));
    }

    public boolean equals(Object other) {
        if (this == other) { return true; }
        return false;
    }

    public void toLowestTerms() {
        int a = this.num;
        int b = this.den;
        int c = 1;
        while (a != 0 && b != 0) {
            c = a % b;
            a = b;
            b = c;
        }
        this.num = this.num / a;
        this.den = this.den / a;

        /*
        int counter;
        boolean foundLowest = false;
        counter = 2;

        while (!foundLowest) {
            if ((this.num % counter) == 0 && (this.den % counter) == 0) {
                this.num = this.num / counter;
                this.den = this.den / counter;
                counter = 2;
            }
            else { counter++; }

            if (counter > 4000) {
                foundLowest = true;
            }
        }
         */
    }

    public static int gcd(int num, int den) {
        int a = num;
        int b = den;
        int c = 1;
        boolean done = false;
        while (a != 0 && b != 0) {
            c = a % b;
            a = b;
            b = c;
        }
        return a;
    }

}
