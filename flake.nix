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
        pkgs = import nixpkgs {inherit system;};
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python312
            uv
            zlib
            gcc
            stdenv.cc.cc.lib
          ];

          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.zlib
            pkgs.stdenv.cc.cc.lib
            pkgs.gcc.cc
          ];
        };
      }
    );
}
