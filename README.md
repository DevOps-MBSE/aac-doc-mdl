# AaC-Doc-Mdl
An AI powered plugin for Architecture-as-Code that supports MBSE document development.

## Concept Notes

Model a document using the standard AaC model schema.  The top level model represents the document and the name of the model is the document title.  Components within that model are teh main sections of the document outline.  The description is an abstract and may include instructions for the AI in generation of the outline.  Behaviors represent content blocks or topics.  Features define expectations of content in the form of acceptance tests.  Since components are just models themselves, each section is modeled in exactly the same way.

This has been developed to support formal document generation and assumes there is guidance that must be adhered to for the document.  My modeling your document you have an unambiguous definition of the structure and scope allocation for your document.  You can tailor the content in achievement of the structure and requirements by specifying your thoughts in the model descriptions and test specifications.  This should allow you to more rapidly employ engineering rigor in your document creation and allow you to generate Gherkin automated tests which can employ AI as your automated testing assistant for documentation.  

Perhaps in the future we'll adapt this plugin to establish an explicit `document` schema that would just tweak the fields of `model` to be more aligned to document modeling.  Such a change would replace the `components` field with `sections` and `behaviors` with `content`.  It may even allow you to specify the output file directly in the model for traceability.  There's even the possibility of standardizing the testing so that it could be performed by AaC without additional test code needing to be created.

### Commands

#### gen-doc-outline

This is intended to support the initial outline development and review for a document.  Assuming you're working within a team, it's always a good idea to develop the concept for your document as an outline and get feedback from your peers.  This allows you to think through how content is allocated and establish a good narrative flow.  The outline does not attempt to provide document content, only describe the content to be included.  We do this by providing an abstract for each section of the document.

  - Let's assume I've built my document model, assigned requirements, written my acceptance tests, and may have added thoughts to the description.
  - I can then run `aac gen-doc-outline` to output the following:
    - A markdown file containing document body text.  The title is a level one heading at the top.  The AI generated abstract is followed by a table with linked requirement ID, requirement text, and acceptance test (if present).
    - A rendered PDF of the generated markdown file.
    - An `aac_evaluate` file replicating the model but replacing the descriptions with AI generated abstracts.  This is disabled by default, but can be enabled with a CLI flag.
  - The `temperature` passed into the AI for abstract generation should be very low.  This is not where we want "flowery" language.

##### Example Output

```markdown
# Model Name as Title

**Abstract:**  This is the abstract for this portion of the modeled document.  It is AI generated and should be carefully reviewed by humans before going forward.

**Allocated Requirements**
| Req ID  | Shall Statement |
|----|----|
| REQ-001 | The document shall be amazing. |
| REQ-002 | The document shall be AI generated. |

**Test Specifications**

| Req ID  | Shall Statement |
|----|----|
| REQ-001 | The document shall show test specific requirements. |  

**Test Title**
- Given
    - The sky is blue
    - Unicorns rome the plains
- When
    - You read the document
- Then
    - You are amazed by the content
    - You are left in a zen like state
```

#### gen-doc-draft

This is intended to help you create the draft content for your document after you've got your outline in place and agreed to with peers and stakeholders.  It's a good idea to get reviews from your peers in the content creation process to improve quality and ensure compliance by incorporating multiple perspectives.  You can use feedback to adjust your model and regenerate the draft or just adjust the output and configuration manage it as your deliverable.

  - Let's assume I've built my document model, assigned requirements, written my acceptance tests, and captured a good abstract in the description.
  - I can then run `aac gen-doc-draft` to output the following:
    - A markdown file containing document content.  The title is a level one heading at the top.  Each section has the AI generated document test followed by a table with linked requirement ID, requirement text, and acceptance test (if present).
    - A rendered PDF of the generated markdown file.
  - The `temperature` passed into the AI for abstract generation should be low, but a bit higher than abstract generation.  We still don't want "flowery" language, but a bit more "creativity" may be valuable.

##### Example Output

```markdown
# Model Name as Title

This is the content for this portion of the modeled document.  Since this is just a draft, we'll continue to provide supporting requirements and test specification information to help reviewers evaluate the content.  It is AI generated and should be carefully reviewed by humans before going forward.

**Allocated Requirements**
| Req ID  | Shall Statement |
|----|----|
| REQ-001 | The document shall be amazing. |
| REQ-002 | The document shall be AI generated. |

**Test Specifications**

| Req ID  | Shall Statement |
|----|----|
| REQ-001 | The document shall show test specific requirements. |  

**Test Title**
- Given
    - The sky is blue
    - Unicorns rome the plains
- When
    - You read the document
- Then
    - You are amazed by the content
    - You are left in a zen like state
```