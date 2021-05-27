<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:import href="html.xsl" />
    <xsl:output method="xml"/>

    <xsl:template match="statement">
        <div class="exercise-statement"><p><strong><xsl:value-of select="../@checkit-slug"/>.</strong></p><xsl:apply-templates/></div>
    </xsl:template>

    <xsl:template match="answer">
        <div class="exercise-answer">
            <h4>Partial Answer:</h4>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template name="image-based-math"><xsl:param name="latex"/><img><xsl:attribute name="alt">LaTeX: <xsl:value-of select="normalize-space($latex)"/></xsl:attribute><xsl:attribute name="title">LaTeX: <xsl:value-of select="normalize-space($latex)"/></xsl:attribute><xsl:attribute name="data-equation-content"><xsl:value-of select="normalize-space($latex)"/></xsl:attribute></img></xsl:template>

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