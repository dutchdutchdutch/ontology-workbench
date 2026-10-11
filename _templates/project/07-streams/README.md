# 07 Streams: <project>

What goes here: views of how the work runs, keyed to the glossary. Optional, on request. A lens
is laid over the step 06 picture and marks which terms take part in something. A process is its
own picture: who does what, in what order, with every box tied to the glossary terms it uses.

| File | Required | How it gets here |
|---|---|---|
| `<name>.md` | one per value stream | A person writes it, starting from `_stream.template.md`. A hypothesis until `reviewed:` holds a date. |
| `stream-data.js` | when rendered | `tools/render-streams.py <project>` writes it from `../06-ontology/ontology-data.js` and the stream files. |
| `value-streams.html` | when rendered | The same script copies the page next to the data. Open in a browser. |
| `<name>.md` with `process:` | one per process | A person writes it, starting from `_process.template.md`. Same sign-off line. |
| `process-data.js` | when rendered | `tools/render-processes.py <project>` writes it from the process files and `../05-glossary/glossary.md`. |
| `processes.html` | when rendered | The same script copies the page next to the data. Full view, step-by-step walk, sidebar with definitions. |
| `skipped.md` | when not rendered | `tools/render-streams.py <project> --skip "not requested"`. |

The page carries two kinds of lens. The workflow lens comes from the glossary's `workflow:` key,
the same one step 06 draws. The value-stream lens comes from the files here: money, data or
results moving between terms the glossary already defines.

Never edit a generated file by hand. Change the authored file, the glossary or the step 06
picture, and render again.

Contract: [../../../factory/steps/07-streams/CONTEXT.md](../../../factory/steps/07-streams/CONTEXT.md)
