package com.example.appengine.springboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.Objects;

@SpringBootApplication
@RestController
public class SpringbootApplication
{

    final String ip = "http://35.228.58.64/";

    public static void main(String[] args)
    {
        SpringApplication.run(SpringbootApplication.class, args);
    }

    @GetMapping("/")
    public String hello()
    {
        return "Hello world!";
    }

    @GetMapping("/{name}")
    public String getRandomNumber(@PathVariable("name") String name)
    {
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response = restTemplate.getForEntity(ip + name, String.class);
        if (response.getStatusCode() != HttpStatus.OK)
        {
            return "Cannot comply, error: " + response.getStatusCode();
        }

        return "Hello, " + name + "! Here is your lucky number: " + response.getBody();
    }
}
