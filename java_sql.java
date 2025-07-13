import java.util.Scanner;

public class java_sql {
public static void main(String[] args) {
    Scanner scanner= new Scanner(System.in);
    System.out.println("Please enter a number of your choice:");
int x= scanner.nextInt();
scanner.close();
int reversed= 0;
if (x<10){
System.out.println("Please enter valid number.");
return;
}
while(x>reversed){
    reversed= reversed * 10 + x % 10;
    x /= 10;
}
if(x==reversed || x== reversed/10){
    System.out.println("This is a palindrome number.");
}
else
System.out.println("This is not a palindrome number.");
}
}