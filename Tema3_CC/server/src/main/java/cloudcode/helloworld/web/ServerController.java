
package cloudcode.helloworld.web;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;
import java.util.Random;

/**
 * defines the REST endpoints managed by the server.
 */
@RestController
public final class ServerController
{
    /**
     * endpoint for the landing page
     * @return a simple hello world message
     */
    @GetMapping(path = "/{name}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<String> get(@PathVariable("name") String name)
    {
        Optional<String> randomNumberOpt = Optional.of(String.valueOf(new Random().nextInt()));
        return ResponseEntity.of(randomNumberOpt);}
}
