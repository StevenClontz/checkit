<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:import href="html.xsl" />
    <xsl:output method="xml"/>

    <xsl:template match="statement">
        <div class="exercise-statement"><p><strong><xsl:value-of select="../@checkit-slug"/>.</strong></p><xsl:apply-templates/></div>
    </xsl:template>

    <xsl:template match="exercise">
      <item>
        <xsl:attribute name="ident"><xsl:value-of select="@checkit-slug"/>-<xsl:value-of select="@checkit-seed"/></xsl:attribute>
        <xsl:attribute name="title"><xsl:value-of select="@checkit-slug"/> | <xsl:value-of select="@checkit-title"/> | ver. <xsl:value-of select="@checkit-seed"/></xsl:attribute>
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>question_type</fieldlabel>
              <fieldentry>file_upload_question</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>
          <material>
            <!-- converts to <mattext texttype="text/html"/> via LXML -->
             <mattextxml><xsl:apply-templates select="statement"/></mattextxml>
          </material>
          <response_str ident="response1" rcardinality="Single">
            <render_fib>
              <response_label ident="answer1" rshuffle="No"/>
            </render_fib>
          </response_str>
        </presentation>
        <itemfeedback ident="general_fb">
          <flow_mat>
            <material>
              <mattextxml><xsl:apply-templates select="answer"/></mattextxml>
            </material>
          </flow_mat>
        </itemfeedback>
      </item>
    </xsl:template>

    <xsl:template match="answer">
        <div class="exercise-answer">
            <h4>Partial Answer:</h4>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template name="image-based-math"><xsl:param name="latex"/><img style="border:1px #ddd solid;padding:5px;border-radius:5px;"><xsl:attribute name="src">https://usaonline.southalabama.edu/equation_images/<xsl:value-of select="normalize-space($latex)"/></xsl:attribute><xsl:attribute name="alt"><xsl:value-of select="normalize-space($latex)"/></xsl:attribute><xsl:attribute name="title"><xsl:value-of select="normalize-space($latex)"/></xsl:attribute><xsl:attribute name="data-latex"><xsl:value-of select="normalize-space($latex)"/></xsl:attribute></img></xsl:template>

    <xsl:template match="me"><p style="text-align:center;"><xsl:call-template name="image-based-math"><xsl:with-param name="latex"><xsl:value-of select="."/></xsl:with-param></xsl:call-template></p></xsl:template>

    <xsl:template match="md">
      <p style="text-align:center;">
        <xsl:call-template name="image-based-math">
          <xsl:with-param name="latex">
\begin{align*} <xsl:apply-templates select="mrow"/> \end{align*}
          </xsl:with-param>
        </xsl:call-template>
      </p>
    </xsl:template>


    <xsl:template match="m"><xsl:call-template name="image-based-math"><xsl:with-param name="latex"><xsl:value-of select="."/></xsl:with-param></xsl:call-template></xsl:template>

</xsl:stylesheet>