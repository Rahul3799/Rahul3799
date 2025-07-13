package com.qa.aal;

import java.time.Duration;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class addToBasket {
    WebDriver driver;


    public addToBasket(WebDriver driver){
        this.driver= driver;
    }

    public void clickToAdd(){
        By size= By.xpath("//body/div[@id='__next']/div[@id='siteLayout']/div[@class='col-span-12 offset']/div[@class='PD___StyledDiv-sc-xi1djx-0 kiucsj']/section[@class='grid grid-cols-2 gap-6 pb-10 border-b border-dashed border-silverSurfer-400']/div[@class='flex flex-col']/section[@class='PackSizeSelector___StyledSection-sc-l9rhbt-0 jFkiCb']/div[@class='w-full']/div[2]/div[1]");
        WebDriverWait wait= new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(ExpectedConditions.elementToBeClickable(size));
        driver.findElement(size).click();
        driver.findElement(By.xpath("//buttton[contains(text(),'Add to basket')]")).click();
        System.out.println("Hi");
    }
}
