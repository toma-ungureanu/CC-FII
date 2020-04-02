package cloudcode.helloworld;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * this class serves as an entry point for the Spring Boot app
 * Here, we check to ensure all required environment variables are set
 */
@SpringBootApplication
public class ServerApp
{

    public static void main(final String[] args)
    {
        String value = System.getenv("PORT");
        if (value == null)
        {
            System.out.println("error: PORT environment variable not set");
            System.exit(1);
        }
        SpringApplication.run(ServerApp.class, args);
    }
}
