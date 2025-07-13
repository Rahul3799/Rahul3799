package com.qa.aal;
import java.time.Duration;
import java.util.*;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;


public class App 
{
    static WebDriver driver = new EdgeDriver();
    public static void main( String[] args ) throws InterruptedException
    {
        WebDriverWait wait= new WebDriverWait(driver, Duration.ofSeconds(10));
        JavascriptExecutor js= (JavascriptExecutor) driver;
        String url= "https://www.bigbasket.com/";
        driver.get(url);
        driver.manage().window().fullscreen();
        Thread.sleep(8000);
        By ele= By.xpath("//a[normalize-space()='About Us']");
        js.executeScript("arguments[0].scrollIntoView(true);", ele);
        // wait.until(ExpectedConditions.elementToBeClickable(ele));
        driver.findElement(ele).click();
        String title= driver.getTitle();
        driver.findElement(ele).click();
        System.out.println(title);
        Set<String> windowHandles= driver.getWindowHandles();
        System.out.println(windowHandles);
        // js.executeScript("window.scrollBy(0,500)");
            
        // addToBasket add= new addToBasket(driver);
        // add.clickToAdd();

        System.out.println( "Hello World!" );
        Thread.sleep(3000);
        driver.quit();
    }
}
