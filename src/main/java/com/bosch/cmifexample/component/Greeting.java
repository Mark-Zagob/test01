package com.bosch.cmifexample.component;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.node.ObjectNode;
import lombok.Getter;
import lombok.Setter;
import org.springframework.http.HttpStatusCode;

public class Greeting {
    public Greeting(HttpStatusCode c, ObjectNode b) {
        setGreetCode(c);
        setGreetMessage(b);
    }

    @Getter
    @Setter
    @JsonProperty("greetCode")
    private HttpStatusCode greetCode;

    @Getter
    @Setter
    @JsonProperty("greetMessage")
    private ObjectNode greetMessage;

}
