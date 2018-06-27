FROM opensecurity/mobile-security-framework-mobsf
MAINTAINER We45
ENV MOBSF_API_KEY=a9721936158691065633f1a10d899a997f55c5760b57467ad219168ed8672340
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
