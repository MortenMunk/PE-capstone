{
  description = "Development environment for python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
        };
      in {
        devShells.default = with pkgs;
          mkShell {
            buildInputs = [
              python312
              stdenv.cc.cc.lib
              uv
              tk
            ];

            LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib/";
          };
      }
    );
}
