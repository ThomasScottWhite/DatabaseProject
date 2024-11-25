# Database Project

## Environment Setup

### Install Conda

We used [Minforge](https://github.com/conda-forge/miniforge) as our environment manager, but any `conda` installation should work.

Install Miniforge: https://github.com/conda-forge/miniforge/releases


#### Alternative

If you don't feel like downloading Miniforge or some other variation of `conda`, you will need:

1. Python 3.10.15 (any 3.10.x version will probably work) and `pip`
2. `npm` (Node Package Manager)

### Install Podman

We host our database in a podman/docker container, so you will need podman or docker. Podman is recommended as it is what was used when testing/creating the project. Here are instructions for installing podman: https://podman.io/docs/installation

Note: if you are using docker, replace `podman` with `docker` in all future commands.

### Environment Creation

If you have `conda` installed (recommended):

```sh
git clone https://github.com/ThomasScottWhite/DatabaseProject.git
cd ./DatabaseProject
conda env create -f environment.yml -n dbproj
conda activate dbproj
cd ./greek-management-studio-frontend
npm install
cd ../api
podman build --tag dbproj -f db.Containerfile .
```

If you installed Python, `pip`, and `npm` some other way:

```sh
git clone https://github.com/ThomasScottWhite/DatabaseProject.git
cd ./DatabaseProject
pip install -r requirements.txt
cd ./greek-management-studio-frontend
npm install
cd ../api
podman build --tag dbproj -f db.Containerfile .
```

Now, your environment should be ready! Note that the conda method was what was used during development, so it's the recommended method.

## Running the Code

The easiest way to run this code is using three terminal instances: one for the frontend, one for the backend, and one for the database. If you can't open multiple terminals (perhaps you are `ssh`'d into a machine), you can use a terminal multiplexer such as `tmux`.

### Start the Database

In one terminal, run the following command *from within the `DatabaseProject/api/` directory*:

```sh
podman run -p 6789:5432 dbproj
```

This will start the podman container hosting the database, accessible at `localhost:6789`.

### Start the Backend (API)

In another terminal, with the project's `conda` environment activated (unless you are not using `conda`), run the following *from the `DatabaseProject/` directory*:

```sh
python -m api
```

This will start the backend on `localhost:6969`. You can go to <http://localhost:6969/docs> while the backend is running to view auto-generated documentation for the backend.

### Start the Frontend (Web GUI)

In yet another terminal, with the project's `conda` environment activated (unless you are not using `conda`), run the following *from the `DatabaseProject/greek-management-studio-frontend/` directory*:

```sh
npm run dev
```

This will start the frontend on whatever port is printed to the console (likely <http://localhost:5173>).
