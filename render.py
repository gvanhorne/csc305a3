import subprocess

# List of commands to run
commands = [
    "python3 RayTracer.py tests/testImgPlane.txt",
    "python3 RayTracer.py tests/testAmbient.txt",
    "python3 RayTracer.py tests/testBackground.txt",
    "python3 RayTracer.py tests/testBehind.txt",
    "python3 RayTracer.py tests/testIntersection.txt",
    "python3 RayTracer.py tests/testDiffuse.txt",
    "python3 RayTracer.py tests/testShadow.txt",
    "python3 RayTracer.py tests/testSpecular.txt",
    "python3 RayTracer.py tests/testSample.txt",
    "python3 RayTracer.py tests/testParsing.txt",
    "python3 RayTracer.py tests/testIllum.txt",
    "python3 RayTracer.py tests/testReflection.txt"
]

# Run commands sequentially
for command in commands:
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e)
