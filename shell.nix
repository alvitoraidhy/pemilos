{
  pkgs ? import <nixpkgs> {}
}:
pkgs.mkShell {
  name="dev-environment";
  buildInputs = [
    pkgs.python3
    pkgs.python3.pkgs.pip
    pkgs.python3.pkgs.setuptools
  ];
  shellHook =
  ''
    # Tells pip to put packages into $PIP_PREFIX instead of the usual locations.
    # See https://pip.pypa.io/en/stable/user_guide/#environment-variables.
    export PIP_PREFIX=$(pwd)/_build/pip_packages;
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH";
    export PATH="$PIP_PREFIX/bin:$PATH";
    unset SOURCE_DATE_EPOCH;

    echo "Python v3";
    echo "Start developing...";
  '';
}
