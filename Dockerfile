FROM openjdk:17-alpine

WORKDIR /app

COPY ./build/libs/app-pick-server.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
