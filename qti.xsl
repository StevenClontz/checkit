<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:import href="html.xsl" />
    <xsl:output method="xml"/>


    <xsl:template match="exercise">
      <item>
        <xsl:attribute name="ident"><xsl:value-of select="@masterit-slug"/>-<xsl:value-of select="@masterit-seed"/></xsl:attribute>
        <xsl:attribute name="title"><xsl:value-of select="@masterit-slug"/> | <xsl:value-of select="@masterit-name"/> | ver. <xsl:value-of select="@masterit-seed"/></xsl:attribute>
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>question_type</fieldlabel>
              <fieldentry>essay_question</fieldentry>
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
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="me"><p><xsl:call-template name="codecogs-math"><xsl:with-param name="latex"><xsl:value-of select="."/></xsl:with-param></xsl:call-template></p></xsl:template>

    <xsl:template match="md">
      <p>
        <xsl:call-template name="codecogs-math">
          <xsl:with-param name="latex">
            <xsl:choose>
              <xsl:when test="@alignment='alignat'">
\begin{alignat*}{<xsl:value-of select="@alignat-columns"/>} <xsl:apply-templates select="mrow"/> \end{alignat*}
              </xsl:when>
              <xsl:otherwise>
\begin{align*} <xsl:apply-templates select="mrow"/> \end{align*}
              </xsl:otherwise>
            </xsl:choose>
          </xsl:with-param>
        </xsl:call-template>
      </p>
    </xsl:template>

    <xsl:template match="mrow"><xsl:value-of select="."/> \\</xsl:template>

    <xsl:template match="m"><xsl:call-template name="codecogs-math"><xsl:with-param name="latex"><xsl:value-of select="."/></xsl:with-param></xsl:call-template></xsl:template>

</xsl:stylesheet>