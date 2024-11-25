from docker.io/postgres:17

ENV POSTGRES_DB=greek_management_studio
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin

EXPOSE 5432

COPY ./db/sql/*.sql /docker-entrypoint-initdb.d/

# BUILD AND RUN CONTAINER:
# podman build --tag dbproj -f db.Containerfile .
# podman run -p 6789:5432 dbproj
