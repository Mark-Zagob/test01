FROM openjdk:17-slim
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} /app.jar
RUN addgroup -gid 1001 -System app && adduser -uid 1001 -System appuser -gid 1001

USER 1001

EXPOSE 8081
CMD [ "-XshowSettings:vm", \
    "-XX:MaxRAMPercentage=75", \
    "-jar", "/app.jar" ]
ENTRYPOINT [ "java" ]
