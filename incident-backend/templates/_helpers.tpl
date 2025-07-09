{{- define "incident-backend.name" -}}
incident-backend
{{- end }}

{{- define "incident-backend.fullname" -}}
{{ include "incident-backend.name" . }}-{{ .Release.Name }}
{{- end }}

