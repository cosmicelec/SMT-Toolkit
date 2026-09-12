import argparse
import sys
from rich.console import Console
from rich.panel import Panel

# Use relative imports since this is now part of the smt package
from .image_steg import encode_image, decode_image
from .text_steg import encode_text, decode_text
from .audio_steg import encode_audio, decode_audio
from .qr_steg import encode_qr, decode_qr
from .pdf_steg import encode_pdf, decode_pdf
from .git_steg import encode_git, decode_git
from .capacity import get_capacity_report

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="Python Steganography Multi-Tool (SMT)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available modules")
    
    # Common arguments
    def add_common_encode_args(p):
        p.add_argument("--payload", required=True, help="Secret payload to hide")
        p.add_argument("--password", required=True, help="Encryption password")
        
    def add_common_decode_args(p):
        p.add_argument("--password", required=True, help="Decryption password")

    # Image
    img_parser = subparsers.add_parser("image", help="Image Steganography")
    img_subparsers = img_parser.add_subparsers(dest="action", required=True)
    
    img_enc = img_subparsers.add_parser("encode")
    img_enc.add_argument("--file", required=True, help="Input image file")
    img_enc.add_argument("--out", required=True, help="Output image file")
    add_common_encode_args(img_enc)
    
    img_dec = img_subparsers.add_parser("decode")
    img_dec.add_argument("--file", required=True, help="Input image file")
    add_common_decode_args(img_dec)

    # Text
    txt_parser = subparsers.add_parser("text", help="Text Steganography")
    txt_subparsers = txt_parser.add_subparsers(dest="action", required=True)
    
    txt_enc = txt_subparsers.add_parser("encode")
    txt_enc.add_argument("--file", required=True, help="Input text file")
    txt_enc.add_argument("--out", required=True, help="Output text file")
    add_common_encode_args(txt_enc)
    
    txt_dec = txt_subparsers.add_parser("decode")
    txt_dec.add_argument("--file", required=True, help="Input text file")
    add_common_decode_args(txt_dec)
    
    # Audio
    aud_parser = subparsers.add_parser("audio", help="Audio Steganography")
    aud_subparsers = aud_parser.add_subparsers(dest="action", required=True)
    
    aud_enc = aud_subparsers.add_parser("encode")
    aud_enc.add_argument("--file", required=True, help="Input audio file")
    aud_enc.add_argument("--out", required=True, help="Output audio file")
    add_common_encode_args(aud_enc)
    
    aud_dec = aud_subparsers.add_parser("decode")
    aud_dec.add_argument("--file", required=True, help="Input audio file")
    add_common_decode_args(aud_dec)
    
    # QR
    qr_parser = subparsers.add_parser("qr", help="QR Code Steganography")
    qr_subparsers = qr_parser.add_subparsers(dest="action", required=True)
    
    qr_enc = qr_subparsers.add_parser("encode")
    qr_enc.add_argument("--url", required=True, help="Target URL to embed in the QR code")
    qr_enc.add_argument("--out", required=True, help="Output QR image file")
    add_common_encode_args(qr_enc)
    
    qr_dec = qr_subparsers.add_parser("decode")
    qr_dec.add_argument("--file", required=True, help="Input QR image file")
    add_common_decode_args(qr_dec)
    
    # PDF
    pdf_parser = subparsers.add_parser("pdf", help="PDF Steganography")
    pdf_subparsers = pdf_parser.add_subparsers(dest="action", required=True)
    
    pdf_enc = pdf_subparsers.add_parser("encode")
    pdf_enc.add_argument("--file", required=True, help="Input PDF file")
    pdf_enc.add_argument("--out", required=True, help="Output PDF file")
    add_common_encode_args(pdf_enc)
    
    pdf_dec = pdf_subparsers.add_parser("decode")
    pdf_dec.add_argument("--file", required=True, help="Input PDF file")
    add_common_decode_args(pdf_dec)
    
    # Git
    git_parser = subparsers.add_parser("git", help="Git Commit Steganography")
    git_subparsers = git_parser.add_subparsers(dest="action", required=True)
    
    git_enc = git_subparsers.add_parser("encode")
    add_common_encode_args(git_enc)
    
    git_dec = git_subparsers.add_parser("decode")
    add_common_decode_args(git_dec)
    
    # Report
    rep_parser = subparsers.add_parser("report", help="Capacity Report")
    rep_parser.add_argument("--file", required=True, help="File to check capacity for")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    try:
        if args.command == "report":
            console.print(Panel.fit(f"[bold blue]{get_capacity_report(args.file)}[/bold blue]", title="Capacity Report"))
            return

        if args.command == "image":
            if args.action == "encode":
                encode_image(args.file, args.payload, args.password, args.out)
                console.print(f"[bold green]✓[/bold green] Payload successfully hidden in {args.out}")
            else:
                res = decode_image(args.file, args.password)
                console.print(Panel.fit(f"[bold green]{res}[/bold green]", title="Decoded Payload"))
                
        elif args.command == "text":
            if args.action == "encode":
                encode_text(args.file, args.payload, args.password, args.out)
                console.print(f"[bold green]✓[/bold green] Payload successfully hidden in {args.out}")
            else:
                res = decode_text(args.file, args.password)
                console.print(Panel.fit(f"[bold green]{res}[/bold green]", title="Decoded Payload"))
                
        elif args.command == "audio":
            if args.action == "encode":
                encode_audio(args.file, args.payload, args.password, args.out)
                console.print(f"[bold green]✓[/bold green] Payload successfully hidden in {args.out}")
            else:
                res = decode_audio(args.file, args.password)
                console.print(Panel.fit(f"[bold green]{res}[/bold green]", title="Decoded Payload"))
                
        elif args.command == "qr":
            if args.action == "encode":
                encode_qr(args.url, args.payload, args.password, args.out)
                console.print(f"[bold green]✓[/bold green] Payload successfully embedded in QR code at {args.out}")
            else:
                res = decode_qr(args.file, args.password)
                console.print(Panel.fit(f"[bold green]{res}[/bold green]", title="Decoded Payload"))
                
        elif args.command == "pdf":
            if args.action == "encode":
                encode_pdf(args.file, args.payload, args.password, args.out)
                console.print(f"[bold green]✓[/bold green] Payload successfully hidden in PDF at {args.out}")
            else:
                res = decode_pdf(args.file, args.password)
                console.print(Panel.fit(f"[bold green]{res}[/bold green]", title="Decoded Payload"))
                
        elif args.command == "git":
            if args.action == "encode":
                encode_git(args.payload, args.password)
                console.print("[bold green]✓[/bold green] Payload successfully hidden in latest git commit.")
            else:
                res = decode_git(args.password)
                console.print(Panel.fit(f"[bold green]{res}[/bold green]", title="Decoded Payload"))
                
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
