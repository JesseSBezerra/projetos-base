"""Faz `git add` + `git commit` + `git push` da branch atual deste repositório.

Uso:
    python publicar.py "mensagem do commit"
    python publicar.py "mensagem do commit" --branch home-c2-v2
    python publicar.py "mensagem do commit" --remote origin --sem-push

Se não houver nada em staged/unstaged (working tree limpa), o script avisa
e não cria commit vazio.
"""
import argparse
import subprocess
import sys


def rodar(comando, **kwargs):
    print(f"$ {' '.join(comando)}")
    resultado = subprocess.run(comando, text=True, **kwargs)
    if resultado.returncode != 0:
        sys.exit(resultado.returncode)
    return resultado


def branch_atual():
    resultado = subprocess.run(
        ["git", "branch", "--show-current"], text=True, capture_output=True, check=True
    )
    return resultado.stdout.strip()


def ha_mudancas():
    resultado = subprocess.run(
        ["git", "status", "--porcelain"], text=True, capture_output=True, check=True
    )
    return bool(resultado.stdout.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mensagem", help="Mensagem do commit")
    parser.add_argument("--branch", default=None, help="Branch a enviar (default: a atual)")
    parser.add_argument("--remote", default="origin", help="Remote de destino (default: origin)")
    parser.add_argument("--sem-push", action="store_true", help="Só faz add+commit, não envia")
    args = parser.parse_args()

    branch = args.branch or branch_atual()

    rodar(["git", "add", "-A"])

    if not ha_mudancas():
        print("Nada para commitar (working tree limpa).")
    else:
        rodar([
            "git", "commit", "-m",
            f"{args.mensagem}\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>",
        ])

    if args.sem_push:
        print("`--sem-push` passado: pulando o push.")
        return

    rodar(["git", "push", "-u", args.remote, branch])
    print(f"Push concluído: {args.remote}/{branch}")


if __name__ == "__main__":
    main()
