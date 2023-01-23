{
  pkgs ? import <nixpkgs> {}
}:
pkgs.mkShell {
  name="dev-environment";
  buildInputs = [
    # Python
    pkgs.python39
    pkgs.python39.pkgs.pip
    pkgs.python39.pkgs.setuptools
    pkgs.python39.pkgs.virtualenv
    pkgs.python39.pkgs.wheel
  ];
  shellHook =
  ''
    export VIRTUAL_ENV_DISABLE_PROMPT=1;
    unset SOURCE_DATE_EPOCH;

    # Create a virtual environment if it doesn't exist yet
    echo -e "''${YELLOW}Creating python environment...''${NC}"
    virtualenv --no-setuptools .venv > /dev/null
    export PATH=$PWD/venv/bin:$PATH > /dev/null

    # Activate the virtual environment
    source .venv/bin/activate

    # Install all root dependencies
    pip install -r requirements.txt > /dev/null;

    echo "Python v3.9";
    echo "Start developing...";
  '';
}
