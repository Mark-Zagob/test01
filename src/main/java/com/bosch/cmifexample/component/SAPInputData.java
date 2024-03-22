package com.bosch.cmifexample.component;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.node.ObjectNode;
import lombok.Getter;
import lombok.Setter;
import org.springframework.http.HttpStatusCode;

public class SAPInputData {
    public SAPInputData(Object data) {
        setData(data);
    }

    @Getter
    @Setter
    @JsonProperty("sapData")
    private Object data;

}
