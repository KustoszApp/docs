from livereload import Server
from livereload import shell

globs = ("*.rst", "*.md", "*.py", "_static/*", "_templates/*")

if __name__ == "__main__":
    server = Server()
    for glob in globs:
        server.watch(f"source/{glob}", shell("make html"), delay=1)
    server.serve(root="build/html")
